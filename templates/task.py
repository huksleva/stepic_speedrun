from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import re
from dotenv import load_dotenv
from pathlib import Path
import base64

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


def extract_errors_text(driver) -> str:
    """
    Извлекает текст с ошибками из элемента .smart-hints.ember-view.lesson__hint.
    Возвращает очищенный текст для отправки ИИ.
    """
    wait = WebDriverWait(driver, 5)  # Короткий тайм-аут: ошибки появляются быстро

    try:
        # Находим элемент с подсказками об ошибках.
        # Используем точный селектор по трём классам (без пробелов внутри)
        hint_element = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".smart-hints.ember-view.lesson__hint"
        )))

        # Получаем текст через JavaScript (надёжнее для динамического контента)
        raw_text = driver.execute_script("""
            return arguments[0].innerText;
        """, hint_element)

        # === ОЧИСТКА ТЕКСТА ===

        # 1. Убираем лишние пробелы в начале/конце строк
        lines = raw_text.split('\n')
        cleaned_lines = [line.strip() for line in lines]

        # 2. Убираем пустые строки подряд (оставляем максимум 2 переноса)
        text = '\n'.join(cleaned_lines)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # 3. Убираем служебный текст (кнопки, иконки, подсказки интерфейса)
        text = re.sub(r'Скопировать код', '', text)
        text = re.sub(r'💡|⚠️|❌|✅', '', text)  # Убираем эмодзи
        text = re.sub(r'Подсказка:\s*', '', text)  # Убираем префиксы

        # 4. Убираем лишние пробелы между словами
        text = re.sub(r'  +', ' ', text)

        # 5. Финальная обрезка
        text = text.strip()

        if text:
            print(f"✅ Найдена подсказка об ошибке: {text[:100]}...")
            return "\n\nОшибки:\n" + text
        else:
            return ""

    except TimeoutException:
        # Элемент не найден — это нормально, не на всех шагах есть ошибки
        print("ℹ️ Подсказки об ошибках не найдены")
        return ""
    except Exception as e:
        print(f"⚠️ Ошибка при извлечении подсказки: {e}")
        return ""


def encode_image_to_base64(image_path="images") -> str:
    """Кодирует изображение в base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_all_images(driver, save_dir="images") -> list:
    """
    Скачивает все изображения с текущей страницы задания.
    Возвращает список путей к скачанным файлам.
    """
    # Создаём папку для изображений
    Path(save_dir).mkdir(exist_ok=True)

    image_paths = []

    # Находим все <img> в условии задачи
    # (исключаем логотипы и иконки)
    img_elements = driver.find_elements(By.CSS_SELECTOR,
                                        ".problem-statement img, "
                                        ".step-text img, "
                                        ".html-content img, "
                                        ".rich-text-viewer img"
                                        )

    print(f"🔍 Найдено {len(img_elements)} изображений")

    for i, img in enumerate(img_elements):
        try:
            img_url = img.get_attribute("src")

            # Пропускаем:
            # - пустые URL
            # - base64 (уже встроены в страницу)
            # - иконки и логотипы
            if not img_url:
                continue
            if img_url.startswith(""):
                continue
            if "logo" in img_url or "icon" in img_url:
                continue

            # Скачиваем изображение
            response = requests.get(img_url, timeout=10)
            if response.status_code == 200:
                # Определяем расширение
                content_type = response.headers.get("content-type", "")
                if "png" in content_type:
                    ext = "png"
                elif "jpeg" in content_type or "jpg" in content_type:
                    ext = "jpg"
                elif "gif" in content_type:
                    ext = "gif"
                else:
                    ext = "png"  # по умолчанию

                filename = f"task_image_{i}.{ext}"
                filepath = os.path.join(save_dir, filename)

                # Сохраняем
                with open(filepath, "wb") as f:
                    f.write(response.content)

                image_paths.append(filepath)
                print(f"📥 Скачано: {filename}")

        except Exception as e:
            print(f"❌ Ошибка при скачивании изображения: {e}")

    return image_paths


def complete_task(task_text: str, image_paths: list = None) -> str:
    """Получаем ответ от ИИ"""

    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    API_KEY = str(os.getenv("API_KEY"))


    # 🔥 Формируем content: текст + изображения
    # 1. Добавляем текст
    content_parts: list[Any] = [{
        "type": "text",
        "text": task_text
    }]

    # 2. Добавляем изображения (если есть)
    if image_paths:
        for img_path in image_paths:
            if os.path.exists(img_path):
                try:
                    # Определяем тип изображения
                    ext = Path(img_path).suffix.lower()
                    if ext == ".png":
                        mime_type = "image/png"
                    elif ext in [".jpg", ".jpeg"]:
                        mime_type = "image/jpeg"
                    elif ext == ".gif":
                        mime_type = "image/gif"
                    else:
                        mime_type = "image/png"  # по умолчанию

                    # Кодируем в base64
                    base64_image = encode_image_to_base64(img_path)

                    content_parts.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    })
                    print(f"✅ Добавлено изображение: {img_path}")
                except Exception as e:
                    print(f"⚠️ Не удалось добавить {img_path}: {e}")
            else:
                print(f"⚠️ Файл не найден: {img_path}")

    # Минимальный payload — только нужные поля
    payload = {
        "model": "deepseek-ai/DeepSeek-V4-Flash",
        "messages": [
            {
                "role": "system",
                "content": "Ты решаешь задачи для Stepik. Выводи ТОЛЬКО код, без markdown, без ```sql и тд"
            },
            {
                "role": "user",
                "content": content_parts
            }
        ],
        "temperature": 0.1,  # Меньше = точнее код
        "max_tokens": 2048,  # Достаточно для большинства задач
        "stream": False  # Ждём полный ответ
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    print(data)
    text = data['choices'][0]['message']['content']

    try:
        # 1. Убираем открывающий блок (```sql, ```python или просто ```)
        # Паттерн ищет ``` в начале строки, затем язык (опционально), затем перенос строки
        text = re.sub(r'^```\w*\n?', '', text, flags=re.MULTILINE)

        # 2. Убираем закрывающий блок (```) в конце
        text = re.sub(r'\n?```$', '', text, flags=re.MULTILINE)
    except Exception as e:
        print(f"❌   Ошибка выполнения операций со строками:", e)

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


def check_answer(driver, timeout=10) -> bool:
    """
    Ждёт, пока Степик не проверит задание.
    Returns:
        bool: True, если успешно, False, если нет
    """
    # === Проверяем, есть ли "Вы получили" ===
    # Если надпись есть, значит мы на странице с выполненным заданием и можно переходить на следующую страницу
    print("\n🔎 Ожидание ответа компилятора: поиск надписи 'Вы получили'...")
    score_label = None
    wait = WebDriverWait(driver, timeout)
    try:
        score_label = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "span.score-info__score-label"
        )))
        print(f"   ✅ Найдено 'Вы получили'")
    except TimeoutException:
        print(f"   ❌ Не найдено 'Вы получили'")


    # === Проверяем есть ли блок с ошибками ===
    errors_block = None
    try:
        wait = WebDriverWait(driver, timeout)
        # visibility лучше presence: ждёт, пока элемент станет видимым пользователю
        errors_block = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, ".attempt-message_wrong"
        )))
        print(f"   ✅ Найден блок с ошибками")
    except TimeoutException:
        print(f"   ❌ Не найден блок с ошибками")

    # Если задание решено правильно
    if (score_label is not None) and (errors_block is None):
        print(f"✅    Задание решено верно")
        return True
    elif (score_label is None) and (errors_block is not None):
        print(f"❌   Задание решено неверно")
        return False
    else:
        print(f"❌   Неизвестная ошибка")
        exit(0)


def click_try_again_button(driver) -> bool:
    """Кликает на кнопку попробовать снова, если она есть"""
    wait = WebDriverWait(driver, 1)
    try:
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.again-btn")))
        btn.click()
        print("✅ Кнопка 'Попробовать снова' нажата")
        return True
    except TimeoutException:
        print("❌ Кнопка 'Попробовать снова' не найдена")
        return False


def click_send_button(driver) -> bool:
    """
    Находит и нажимает кнопку 'Отправить' на Stepik.
    Возвращает True при правильном ответе на задание, False при ошибке.
    """
    wait = WebDriverWait(driver, 10)
    try:
        # Основной поиск по классу (быстро и стабильно)
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-submission")))
        btn.click()
        print("✅ Кнопка 'Отправить' нажата")
        return True
    except TimeoutException:
        print("⚠️ Кнопка не найдена по классу")
        return False

