from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()


def ai_name_list():
    """Выводит список всех доступных ИИ моделей"""

    ai_url = "https://api.intelligence.io.solutions/api/v1/models?page=1&page_size=50"
    ai_api_key = str(os.getenv("API_KEY"))
    ai_headers = {"Authorization": "Bearer " + ai_api_key}
    ai_response = requests.get(ai_url, headers=ai_headers)
    ai_data = ai_response.json()

    for i in range(len(ai_data["data"])):
        ai_name = ai_data["data"][i]["id"]
        print(ai_name)


def extract_task_text(driver) -> str:
    """
    Извлекает текст задания из элемента .quiz-layout-head.
    Возвращает очищенный текст для отправки ИИ
    """
    wait = WebDriverWait(driver, 10)

    # Находим элемент с заданием
    quiz_element = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".quiz-layout-head"
    )))

    # Способ 1: Получаем через JavaScript (надёжнее для сложного HTML)
    raw_text = driver.execute_script("""
        return arguments[0].innerText;
    """, quiz_element)

    # Способ 2 (альтернатива): quiz_element.text
    # raw_text = quiz_element.text

    # === ОЧИСТКА ТЕКСТА ===

    # 1. Убираем лишние пробелы в начале/конце строк
    lines = raw_text.split('\n')
    cleaned_lines = [line.strip() for line in lines]

    # 2. Убираем пустые строки подряд (оставляем максимум 2 переноса)
    text = '\n'.join(cleaned_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 3. Убираем текст кнопок "Скопировать код" (если остался)
    text = re.sub(r'Скопировать код', '', text)

    # 4. Убираем лишние пробелы между словами
    text = re.sub(r'  +', ' ', text)

    # 5. Финальная обрезка
    text = text.strip()

    return text


def complete_task(task_text) -> str:
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    API_KEY = str(os.getenv("API_KEY"))
    # task_text = "В ответ пиши только код. Задание: Напиши на SQL запрос к БД с названием 'USER' на удаление"

    # Минимальный payload — только нужные поля
    payload = {
        "model": "deepseek-ai/DeepSeek-V4-Flash",
        "messages": [
            {
                "role": "system",
                "content": "Ты решаешь задачи для Stepik. Выводи ТОЛЬКО код, без пояснений, без markdown."
            },
            {
                "role": "user",
                "content": task_text
            }
        ],
        "temperature": 0.1,  # Меньше = точнее код
        "max_tokens": 1024,  # Достаточно для большинства задач
        "stream": False  # Ждём полный ответ
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    text = data['choices'][0]['message']['content']
    print("Ответ от ИИ:\n", text)
    return text


def insert_code_into_editor(driver, code_text: str) -> bool:
    """
    Вставляет код в редактор CodeMirror на Stepik.

    Args:
        driver: WebDriver экземпляр
        code_text: Текст кода для вставки

    Returns:
        bool: True если успешно, False если ошибка
    """
    wait = WebDriverWait(driver, 10)
    try:
        # === СПОСОБ 1: Через JavaScript (надёжнее для CodeMirror) ===
        print("📝 Вставляю код в редактор...")

        driver.execute_script("""
            // Находим редактор CodeMirror
            var editorElement = document.querySelector('.CodeMirror');
            if (editorElement && editorElement.CodeMirror) {
                var editor = editorElement.CodeMirror;
                // Очищаем и вставляем новый код
                editor.setValue('');
                editor.setValue(arguments[0]);
                // Фокусируемся на редакторе
                editor.focus();
                return true;
            }
            return false;
        """, code_text)

        print("✅ Код вставлен через CodeMirror API")
        return True

    except Exception as e:
        print(f"⚠️ Не удалось вставить через CodeMirror API: {e}")

        # === СПОСОБ 2: Fallback — ищем textarea ===
        try:
            print("🔄 Пробую через textarea...")

            # Ищем textarea редактора
            textarea = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "textarea.CodeMirror-input, textarea.code-area__textarea"
            )))

            # Очищаем и вставляем
            textarea.clear()
            textarea.send_keys(code_text)

            print("✅ Код вставлен через textarea")
            return True

        except TimeoutException:
            print("❌ Textarea не найдена")
            return False
        except Exception as e2:
            print(f"❌ Ошибка при вставке через textarea: {e2}")
            return False


def wait_until_task_done(driver) -> bool:
    """
    Ждёт, пока Степик не проверит задание.
    Returns:
        bool: True, если успешно, False, если нет
    """
    # === Проверяем, есть ли "Вы получили" ===
    # Если надпись есть, значит мы на странице с выполненным заданием и можно переходить на следующую страницу
    print("\n🔎 Ожидание ответа компилятора: поиск надписи 'Вы получили'...")
    score_label = None
    wait = WebDriverWait(driver, 30)
    try:
        score_label = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "span.score-info__score-label"
        )))
        print(f"   ✅ Найдено")
        return True
    except TimeoutException:
        print(f"   ❌ Не найдено")
        return False


def click_try_again_button(driver):
    """Кликает на кнопку попробовать снова, если она есть"""
    try:
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.again-btn")))
        btn.click()
        print("✅ Кнопка 'Попробовать снова' нажата")
        return wait_until_task_done(driver)  # Проверяем правильный ли код отослал ИИ
    except TimeoutException:
        print("❌ Кнопка 'Попробовать снова' не найдена")
        return False


def click_send_button(driver) -> bool:
    """
    Находит и нажимает кнопку 'Отправить' на Stepik.
    Возвращает True при правильном ответе на задание, False при ошибке.
    """
    wait = WebDriverWait(driver, 10)
    btn = None
    try:
        # Основной поиск по классу (быстро и стабильно)
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-submission")))
        btn.click()
        print("✅ Кнопка 'Отправить' нажата")
        return wait_until_task_done(driver)  # Проверяем правильный ли код отослал ИИ
    except TimeoutException:
        print("⚠️ Кнопка не найдена по классу")
        return False
