from selenium import webdriver
import os
from selenium.webdriver.support.wait import WebDriverWait
from templates.enter_next_page import next_page
from templates.wait_fun import wait_for_network_idle

# === НАСТРОЙКИ ===
# Ссылка на сайт
url = "https://stepik.org/lesson/297514/step/2?unit=279274"

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

    # Ждём, пока загрузятся все элементы страницы
    wait_for_network_idle(driver)

    # Переходим на следующую страницу
    next_page(driver)






    input("⏸️ Нажмите Enter для закрытия...")







