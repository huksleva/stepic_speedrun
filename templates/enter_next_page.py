"""Определяет выполнено ли задание на странице и если так, то переходит на следующую страницу"""
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def next_page(driver):
    """Определяем выполнено задание или нет и если да, то переходим на следующую страницу."""

    # Ждём загрузку элементов страницы до 30 секунд
    wait = WebDriverWait(driver, 30)

    # Ищем элементы:
    # 1. Вкладка "Решения"
    try:
        solutions_tab = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//li[contains(@class, 'discussions_tab')]//a[.//span[text()='Решения']]"
        )))
        variant_1 = True
    except TimeoutException:
        variant_1 = False

    # 2. Надпись "Вы получили:"
    try:
        score_label = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//span[contains(@class, 'score-info__score-label') and contains(., 'Вы получили')]"
        )))
        variant_2 = True
    except TimeoutException:
        variant_2 = False

    # 3. Надпись "Мои решения"
    try:
        my_solutions = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class, 'ember-view') and contains(text(), 'Мои решения')]"
        )))
        variant_3 = True
    except TimeoutException:
        variant_3 = False

    # 4. Наличие двух кнопок "Следующий шаг"
    # Или одной кнопки "Следующий шаг" и одной кнопки "Далее"
    # Любая кнопка/ссылка с текстом "Следующий шаг"

    # === ВАРИАНТ 1: Кнопка "Следующий шаг" + Ссылка "Следующий шаг" ===
    try:
        # Ищем кнопку с "Следующий шаг"
        btn_next_step = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//button[contains(@class, 'lesson_next-btn')]//span[contains(text(), 'Следующий шаг')]"
        )))

        # Ищем ссылку с "Следующий шаг"
        link_next_step = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//a[contains(text(), 'Следующий шаг')]"
        )))

        variant_4_1 = True
        print("✅ Вариант 1: Найдены обе кнопки 'Следующий шаг'")
    except TimeoutException:
        variant_4_1 = False

    # === ВАРИАНТ 2: Кнопка "Дальше" + Ссылка "Следующий шаг" ===
    try:
        # Ищем кнопку с "Дальше" или "Далее"
        btn_next_mobile = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//button[contains(@class, 'lesson_next-btn')]//span[contains(text(), 'Дальше') or contains(text(), 'Далее')]"
        )))

        # Ищем ссылку с "Следующий шаг"
        link_next_step = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//a[contains(text(), 'Следующий шаг')]"
        )))

        variant_4_2 = True
        print("✅ Вариант 2: Найдены кнопки 'Дальше/Далее' и 'Следующий шаг'")

    except TimeoutException:
        variant_4_2 = False

    # === ПРОВЕРКА: Выполняется ли хотя бы один вариант? ===
    if variant_4_1 or variant_4_2:
        variant_4 = True
        print("✅ Задание выполнено! Найден хотя бы один из вариантов кнопок.")
    else:
        variant_4 = False
        print("❌ Задание НЕ выполнено. Кнопки не найдены.")



    # Проверяем выполнено задание или нет
    if variant_1 * variant_2 * variant_3 * variant_4:
        # Если выполнено, то жмём на кнопку "Следующий шаг" или "далее"
        if variant_4_1:
            btn_next_step.click()
        elif variant_4_2:
            btn_next_mobile.click()
    else:
        pass




