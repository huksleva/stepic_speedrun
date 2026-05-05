from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def next_page(driver):
    """Определяет выполнено ли задание на странице и если так, то переходит на следующую страницу"""

    print("\n" + "=" * 60)
    print("🔍 Функция next_page() запущена")
    print(f"📍 URL: {driver.current_url}")
    print("=" * 60)

    # === ШАГ 1: Проверяем, есть ли "Вы получили" ===
    print("\n[1/2] 🔎 Поиск надписи 'Вы получили'...")

    wait = WebDriverWait(driver, 15)

    try:
        score_label = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "span.score-info__score-label"
        )))
        print(f"   ✅ Найдено")
    except TimeoutException:
        print(f"   ❌ Не найдено")

    # === ШАГ 2: Ищем и кликаем "Следующий шаг" ===
    print("\n[2/2] 🔎 Поиск кнопки 'Следующий шаг'...")

    clicked = False
    # Пробуем найти кнопку или ссылку с текстом "Следующий шаг"
    try:
        print(f"   • Пробуем XPath: //button[contains(., 'Следующий шаг')]")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Следующий шаг')]")))

        # Кликаем
        try:
            button.click()
            print(f"   ✅ Клик выполнен")
        except Exception as e:
            driver.execute_script("arguments[0].click();", button)
            print(f"   ✅ Клик выполнен (через JavaScript)")

        clicked = True
    except TimeoutException:
        print(f"   ❌ Не найдено")
    except Exception as e:
        print(f"   ⚠️ Ошибка: {type(e).__name__}: {e}")

    if not clicked:
        print("\n❌ Кнопка 'Следующий шаг' НЕ найдена")
    else:
        print("\n✅ Успешно перешли на следующий шаг!")

    print("=" * 60 + "\n")
    return clicked
