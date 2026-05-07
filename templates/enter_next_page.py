from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import set_key, load_dotenv, find_dotenv


# Вспомогательные функции проверки наличия элемента на странице
def wait_h2(driver, timeout=30):
    """Ждёт заголовок <h2>"""
    wait = WebDriverWait(driver, timeout)
    try:
        # Ждём появления ЛЮБОГО <h2>
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        print("✅ Страница загрузилась")
    except TimeoutException:
        print("❌ Страница не загрузилась")


def solution_label_element(driver, timeout=0.2):
    """Ждёт вкладку 'Решения' и возвращает её"""
    wait = WebDriverWait(driver, timeout)
    print("\n[1/5] 🔎 Поиск вкладки 'Решения'...")
    solution_label = None
    try:
        solution_label = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "span[data-tooltip-pos='top-start']"
        )))
        print(f"   ✅ Найдено")
    except TimeoutException:
        print(f"   ❌ Не найдено")
    finally:
        return solution_label


def score_label_element(driver, timeout=0.2):
    """Ждёт надпись 'Вы получили' и возвращает её"""
    wait = WebDriverWait(driver, timeout)
    print("\n[2/5] 🔎 Поиск надписи 'Вы получили'...")
    score_label = None
    try:
        score_label = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "span.score-info__score-label"
        )))
        print(f"   ✅ Найдено")
    except TimeoutException:
        print(f"   ❌ Не найдено")
    finally:
        return score_label


def score_not_available_element(driver, timeout=0.2):
    """Ждёт надпись 'Баллы не начисляются за эту задачу' и возвращает её"""
    wait = WebDriverWait(driver, timeout)
    print("\n[3/5] 🔎 Поиск надписи 'Баллы не начисляются за эту задачу'...")
    score_not_available = None
    try:
        score_not_available = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".score-info.attempt__score-info"
        )))
        print(f"   ✅ Найдено")
    except TimeoutException:
        print(f"   ❌ Не найдено")
    finally:
        return score_not_available


def my_solutions_label_element(driver, timeout=0.2):
    """Ждёт надпись 'Мои решения' и возвращает её"""
    wait = WebDriverWait(driver, timeout)
    print("\n[4/5] 🔎 Поиск надписи 'Мои решения'...")
    my_solutions_label = None
    try:
        my_solutions_label = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//a[text()='Мои решения']"
        )))
        print(f"   ✅ Найдено")
    except TimeoutException:
        print(f"   ❌ Не найдено")
    finally:
        return my_solutions_label


def next_button_element(driver, timeout=0.2):
    """Ждёт кнопку 'Следующий шаг' и возвращает её"""
    wait = WebDriverWait(driver, timeout)
    print("\n[5/5] 🔎 Поиск кнопки 'Следующий шаг'...")
    button = None
    # Пробуем найти кнопку или ссылку с текстом "Следующий шаг"
    try:
        print(f"   • Пробуем XPath: //button[contains(., 'Следующий шаг')]")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Следующий шаг')]")))
    except TimeoutException:
        print(f"   ❌ Не найдено")
    except Exception as e:
        print(f"   ⚠️ Ошибка: {type(e).__name__}: {e}")
    finally:
        return button


def update_env(key="MY_KEY", value="new_value"):
    """Перезаписывает переменную в .env файле"""
    filepath = find_dotenv()
    set_key(filepath, key, value, quote_mode="always")
    load_dotenv(override=True)
    print(f"✅ {key} обновлён в .env")


# Главная функция
def next_page(driver):
    """
    Определяет выполнено ли задание на странице и если так, то переходит на следующую страницу.
    При успешном переходе на следующую страницу возвращает True, иначе False.
    """

    print("\n" + "=" * 60)
    print("🔍 Функция next_page() запущена")
    old_url = driver.current_url  # ← Запоминаем текущий URL
    print(f"📍 URL: {driver.current_url}")
    print("=" * 60)

    # Ждём пока загрузится страница. Смотрим на <h2>
    wait_h2(driver)

    # === ШАГ 1: Проверяем, есть ли вкладка "Решения" ===
    # Если вкладка есть, значит м ы на странице с заданием или тестом
    # Если нет, то на информативной странице и можно переходить дальше
    solution_label = solution_label_element(driver)

    # === ШАГ 2: Проверяем, есть ли "Вы получили" ===
    # Если надпись есть, значит мы на странице с выполненным заданием и можно переходить на следующую страницу
    score_label = score_label_element(driver)

    # === ШАГ 3: Проверяем, есть ли "Баллы не начисляются за эту задачу" ===
    # Если надпись есть, значит мы на странице с выполненным заданием и можно переходить на следующую страницу
    score_not_available = score_not_available_element(driver)

    # === ШАГ 4: Проверяем, есть ли "Мои решения" ===
    # Если надпись есть, значит мы на странице с выполненным заданием и можно переходить на следующую страницу
    my_solutions_label = my_solutions_label_element(driver)

    # === ШАГ 5: Ищем кнопку "Следующий шаг" ===
    next_button = next_button_element(driver)

    # Если на информативной странице, то кликаем "Следующий шаг"
    # Или если задание выполнено, то тоже жмём "Следующий шаг"
    # Если находимся на странице с выполненным заданием без оценки, так как есть "Мои решения" и "Баллы не начисляются за эту задачу"
    if (solution_label is None) or (score_label is not None) or (
            (score_not_available is not None) and (my_solutions_label is not None)):
        print(f"    Страница информативная или уже с выполненным заданием или с заданием без оценки")
        try:
            next_button.click()
            print(f"   ✅ Клик выполнен")
        except Exception as e:
            driver.execute_script("arguments[0].click();", next_button)
            print(f"   ✅ Клик выполнен (через JavaScript)")
            print(f"    ⚠️ Ошибка:", e)
        print("=" * 60 + "\n")

        # === ⚠️ ЖДЁМ ПЕРЕХОДА НА НОВУЮ СТРАНИЦУ ===
        print("\n⏳ Ожидание перехода на новую страницу...")
        try:
            wait = WebDriverWait(driver, 30)
            # Ждём, пока URL изменится
            wait.until(lambda d: d.current_url != old_url)
            print(f"   ✅ URL изменился: {driver.current_url}")

            # Дополнительно: ждём загрузки новой страницы
            wait_h2(driver)
            return True
        except TimeoutException:
            print("   ⚠️ URL не изменился за 30 сек — это последний шаг!")
            exit(0)

    # Если есть вкладка "Решения" и нет надписи "Вы получили", то мы на странице с нерешённым заданием
    elif (solution_label is not None) and (score_label is None):
        return False
    else:
        print("Неизвестная ошибка!!!")
        exit(0)
