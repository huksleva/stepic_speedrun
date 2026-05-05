from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    wait = WebDriverWait(driver, 30)
    try:
        # Ждём появления ЛЮБОГО <h2>
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        print("✅ Страница загрузилась")
    except TimeoutException:
        print("❌ Страница не загрузилась")



    wait = WebDriverWait(driver, 1)

    # === ШАГ 1: Проверяем, есть ли вкладка "Решения" ===
    # Если вкладка есть, значит м ы на странице с заданием или тестом
    # Если нет, то на информативной странице и можно переходить дальше
    print("\n[1/4] 🔎 Поиск вкладки 'Решения'...")
    solution_label = None
    try:
        solution_label = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "span[data-tooltip-pos='top-start']"
        )))
        print(f"   ✅ Найдено")
    except TimeoutException:
        print(f"   ❌ Не найдено")


    # === ШАГ 2: Проверяем, есть ли "Вы получили" ===
    # Если надпись есть, значит мы на странице с выполненным заданием и можно переходить на следующую страницу
    print("\n[2/4] 🔎 Поиск надписи 'Вы получили'...")
    score_label = None
    try:
        score_label = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "span.score-info__score-label"
        )))
        print(f"   ✅ Найдено")
    except TimeoutException:
        print(f"   ❌ Не найдено")


    # === ШАГ 3: Проверяем, есть ли "Мои решения" ===
    # Если надпись есть, значит мы на странице с выполненным заданием и можно переходить на следующую страницу
    print("\n[3/4] 🔎 Поиск надписи 'Мои решения'...")
    my_solutions_label = None
    try:
        my_solutions_label = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//a[text()='Мои решения']"
        )))
        print(f"   ✅ Найдено")
    except TimeoutException:
        print(f"   ❌ Не найдено")


    # === ШАГ 4: Ищем кнопку "Следующий шаг" ===
    print("\n[4/4] 🔎 Поиск кнопки 'Следующий шаг'...")
    button = None
    # Пробуем найти кнопку или ссылку с текстом "Следующий шаг"
    try:
        print(f"   • Пробуем XPath: //button[contains(., 'Следующий шаг')]")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Следующий шаг')]")))

    except TimeoutException:
        print(f"   ❌ Не найдено")
    except Exception as e:
        print(f"   ⚠️ Ошибка: {type(e).__name__}: {e}")



    # Если на информативной странице, то кликаем "Следующий шаг"
    # Или если задание выполнено, то тоже жмём "Следующий шаг"
    if (solution_label is None) or ((score_label is not None) or (my_solutions_label is not None)):
        print(f"    Страница информативная или уже с выполненным заданием")
        try:
            button.click()
            print(f"   ✅ Клик выполнен")
        except Exception as e:
            driver.execute_script("arguments[0].click();", button)
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
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            print("   ✅ Новая страница загружена")
            return True

        except TimeoutException:
            print("   ⚠️ URL не изменился за 10 сек — возможно, это последний шаг!")
            return False

    # Если есть вкладка "Решения" и нет надписи "Вы получили", то мы на странице с нерешённым заданием
    elif (solution_label is not None) and (score_label is None):
        return False
    else:
        print("Неизвестная ошибка!!!")
        exit(0)

