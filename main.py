from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# === НАСТРОЙКИ ===
# Ссылка на сайт
url = "https://stepik.org/lesson/297514/step/6?unit=279274"

# ⚙️ НАСТРОЙКИ ПРОФИЛЯ
# Путь к НОВОМУ профилю (создастся автоматически при первом запуске)
NEW_PROFILE_PATH = r"C:\Users\Leonid\AppData\Local\Google\Chrome\User Data\SeleniumProfile"
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={NEW_PROFILE_PATH}")
# profile-directory не указываем — будет использоваться профиль по умолчанию в этой папке


# 🕵️ УЛУЧШЕННОЕ СКРЫТИЕ АВТОМАТИЗАЦИИ
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")



# Инициализация драйвера (Chrome по умолчанию)
with webdriver.Chrome(options=options) as driver:
    print("🚀 Запуск Chrome с новым профилем...")
    print(f"📂 Путь к профилю: {NEW_PROFILE_PATH}")

    if not os.path.exists(NEW_PROFILE_PATH):
        print("ℹ️ Профиль будет создан автоматически при первом запуске")

    # Переход на страницу (блокирует до полной загрузки)
    driver.get(url)
    # Проверка статуса загрузки DOM
    ready_state = driver.execute_script("return document.readyState")
    if ready_state != "complete":
        print(f"⚠️ Статус загрузки: {ready_state}")
    print(f"📄 Страница: {driver.title}")
    print("\n💡 Войдите в аккаунт вручную — сессия сохранится для следующих запусков!")

    # Ждём элементы до 30 секунд
    wait = WebDriverWait(driver, 30)
    # Ищем кнопку "Далее"
    button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.lesson_next-btn")
    ))
    # Кликаем по ней
    if button:
        print("✅ Кнопка найдена!")
        button.click()
        print("🔘 Клик выполнен!")
    else:
        print("❌ Кнопка не найдена")






    input("⏸️ Нажмите Enter для закрытия...")







