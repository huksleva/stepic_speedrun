from selenium import webdriver
import os
from templates.enter_next_page import next_page
from templates.task import (
    extract_task_text,
    complete_task,
    insert_code_into_editor,
    click_send_button,
    click_try_again_button
)
from dotenv import load_dotenv
import time

load_dotenv()





# === НАСТРОЙКИ ===
# Ссылка на первую страницу курса Степика
url = str(os.environ.get("START_URL"))

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
        print("\nℹ️ Профиль будет создан автоматически при первом запуске")
        print("💡 Войдите в аккаунт вручную — сессия сохранится для следующих запусков!\n")

    # Переход на страницу (блокирует до полной загрузки)
    driver.get(url)
    print(f"📄 Страница: {driver.title}")


    # Начинаем решать
    is_on_task = True
    while True:
        # Идём до страницы с заданием
        # Если попадаем на страницу с нерешённым заданием
        if not next_page(driver):
            task_text = extract_task_text(driver) # Получаем текст задания
            answer = complete_task(task_text) # Получаем ответ от ИИ
            click_try_again_button(driver) # Нажимаем кнопку "Попробовать снова", если она есть
            time.sleep(0.3)
            insert_code_into_editor(driver, answer) # Вставляем ответ в форму
            time.sleep(0.3)
            click_send_button(driver) # Жмём кнопку "Отправить"


        # Если дошли до конца
        #if is_end(driver):
        #    break

    input("⏸️ Нажмите Enter для завершения работы приложения...")







