"""Определяет выполнено ли задание на странице и если так, то переходит на следующую страницу"""
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # ← Добавлено для замеров времени


def next_page(driver):
    """Определяем выполнено задание или нет и если да, то переходим на следующую страницу."""

    print("\n" + "="*60)
    print("🔍 Функция next_page() запущена")
    print(f"📍 Текущий URL: {driver.current_url}")
    print("="*60)

    # Ждём загрузку элементов страницы до 30 секунд
    wait = WebDriverWait(driver, 30)
    start_time = time.time()

    # === 1. Вкладка "Решения" ===
    print("\n[1/4] 🔎 Поиск вкладки 'Решения'...")
    try:
        solutions_tab = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//li[contains(@class, 'discussions_tab')]//a[.//span[text()='Решения']]"
        )))
        print(f"   ✅ Найдено за {time.time() - start_time:.1f} сек")
        variant_1 = True
    except TimeoutException:
        print(f"   ❌ НЕ найдено за 30 сек (таймаут)")
        variant_1 = False

    # === 2. Надпись "Вы получили:" ===
    print(f"\n[2/4] 🔎 Поиск надписи 'Вы получили'...")
    try:
        score_label = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//span[contains(@class, 'score-info__score-label') and contains(., 'Вы получили')]"
        )))
        print(f"   ✅ Найдено за {time.time() - start_time:.1f} сек")
        variant_2 = True
    except TimeoutException:
        print(f"   ❌ НЕ найдено за 30 сек (таймаут)")
        variant_2 = False

    # === 3. Надпись "Мои решения" ===
    print(f"\n[3/4] 🔎 Поиск ссылки 'Мои решения'...")
    try:
        my_solutions = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class, 'ember-view') and contains(text(), 'Мои решения')]"
        )))
        print(f"   ✅ Найдено за {time.time() - start_time:.1f} сек")
        variant_3 = True
    except TimeoutException:
        print(f"   ❌ НЕ найдено за 30 сек (таймаут)")
        variant_3 = False

    # === 4. Кнопки перехода ===
    print(f"\n[4/4] 🔎 Поиск кнопок перехода...")

    # === ВАРИАНТ 1: Кнопка "Следующий шаг" + Ссылка "Следующий шаг" ===
    print("   └─ Вариант 1: 'Следующий шаг' (кнопка + ссылка)")
    try:
        print("      • Поиск кнопки 'Следующий шаг'...")
        btn_next_step = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//button[contains(@class, 'lesson_next-btn')]//span[contains(text(), 'Следующий шаг')]"
        )))
        print("        ✅ Кнопка найдена")

        print("      • Поиск ссылки 'Следующий шаг'...")
        link_next_step = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//a[contains(text(), 'Следующий шаг')]"
        )))
        print("        ✅ Ссылка найдена")

        variant_4_1 = True
        print("   ✅ Вариант 1: ПОДТВЕРЖДЁН")
    except TimeoutException as e:
        print(f"   ❌ Вариант 1: НЕ подтверждён (таймаут)")
        variant_4_1 = False

    # === ВАРИАНТ 2: Кнопка "Дальше" + Ссылка "Следующий шаг" ===
    print("   └─ Вариант 2: 'Дальше/Далее' (кнопка) + 'Следующий шаг' (ссылка)")
    try:
        print("      • Поиск кнопки 'Дальше' или 'Далее'...")
        btn_next_mobile = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//button[contains(@class, 'lesson_next-btn')]//span[contains(text(), 'Дальше') or contains(text(), 'Далее')]"
        )))
        print("        ✅ Кнопка найдена")

        # Ссылку ищем заново, если в варианте 1 не искали или не нашли
        if 'link_next_step' not in locals():
            print("      • Поиск ссылки 'Следующий шаг'...")
            link_next_step = wait.until(EC.presence_of_element_located((
                By.XPATH,
                "//a[contains(text(), 'Следующий шаг')]"
            )))
            print("        ✅ Ссылка найдена")

        variant_4_2 = True
        print("   ✅ Вариант 2: ПОДТВЕРЖДЁН")
    except TimeoutException:
        print(f"   ❌ Вариант 2: НЕ подтверждён (таймаут)")
        variant_4_2 = False

    # === Итоговая проверка кнопок ===
    if variant_4_1 or variant_4_2:
        variant_4 = True
        print("\n✅ Кнопки перехода: НАЙДЕНЫ")
    else:
        variant_4 = False
        print("\n❌ Кнопки перехода: НЕ найдены")

    # === СВОДКА ===
    total_time = time.time() - start_time
    print("\n" + "-"*60)
    print("📊 СВОДКА ПОИСКА:")
    print(f"   [1] Вкладка 'Решения':        {'✅' if variant_1 else '❌'}")
    print(f"   [2] Надпись 'Вы получили':    {'✅' if variant_2 else '❌'}")
    print(f"   [3] Ссылка 'Мои решения':     {'✅' if variant_3 else '❌'}")
    print(f"   [4] Кнопки перехода:          {'✅' if variant_4 else '❌'}")
    print(f"   ⏱️  Общее время: {total_time:.1f} сек")
    print("-"*60)

    # === ДЕЙСТВИЕ ===
    all_variants = variant_1 and variant_2 and variant_3 and variant_4

    if all_variants:
        print("\n🎯 Задание выполнено! Переходим на следующую страницу...")
        try:
            if variant_4_1 and 'btn_next_step' in locals():
                print("   🔘 Кликаем на кнопку 'Следующий шаг'...")
                btn_next_step.click()
                print("   ✅ Клик выполнен")
            elif variant_4_2 and 'btn_next_mobile' in locals():
                print("   🔘 Кликаем на кнопку 'Дальше/Далее'...")
                btn_next_mobile.click()
                print("   ✅ Клик выполнен")
            else:
                print("   ⚠️ Кнопки найдены, но переменные не определены")
        except Exception as e:
            print(f"   ❌ Ошибка при клике: {type(e).__name__}: {e}")
    else:
        print("\n⏳ Задание ещё НЕ выполнено. Ожидаем...")

    print("="*60 + "\n")
    return all_variants  # ← Возвращаем результат для внешней логики