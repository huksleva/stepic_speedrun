from selenium import webdriver
import os
from templates.enter_next_page import next_page
from templates.task import (
    extract_task_text,
    complete_task,
    insert_code_into_editor,
    click_send_button,
    click_try_again_button,
    check_answer,
    extract_errors_text
)
from templates.clean import kill_all_chrome
from templates.bool_fun import is_end
from dotenv import load_dotenv
from pathlib import Path
import time

load_dotenv()

# Закрываем chrom перед началом
kill_all_chrome()

# === НАСТРОЙКИ ===
# Ссылка на первую страницу курса Степика
url = str(os.environ.get("START_URL"))
# Путь к НОВОМУ профилю (создастся автоматически при первом запуске)
PROFILE_DIR_NAME = "SeleniumProfile"
NEW_PROFILE_PATH = str(os.environ.get("CHROME_PROFILE_PATH")) + PROFILE_DIR_NAME

# ⚙️ НАСТРОЙКИ ПРОФИЛЯ
options = webdriver.ChromeOptions()

# 🕵️ УЛУЧШЕННОЕ СКРЫТИЕ АВТОМАТИЗАЦИИ
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")

# 🔥 Если запускаемся в Docker — включаем headless
if os.environ.get("CHROME_HEADLESS") == "true":
    options.add_argument("--headless=new")  # Новый headless режим
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    print("🐳 Запуск в Docker (headless mode)")
else:
    # Локальный запуск
    options.add_argument(f"--user-data-dir={NEW_PROFILE_PATH}")
    # Если запуск в первый раз (папки SeleniumProfile не существует)
    if not Path(NEW_PROFILE_PATH).is_dir():
        print("ℹ️ При использовании приложения лучше не пользоваться chrome browser ℹ️")
        print("📂 Путь к профилю:", NEW_PROFILE_PATH)
        print("🚀 При первом запуске необходимо авторизоваться в своём аккаунте в Степик, также примите все куки")
        print("Открытие ссылки:", url, "\n")
        with webdriver.Chrome(options=options) as driver:
            # Переход на страницу (блокирует до полной загрузки)
            driver.get(url)
            print(f"📄 Страница: {driver.title}")
            input("⏸️ После окончания регистрации нажмите Enter, чтобы продолжить\n")

# Инициализация драйвера (Chrome по умолчанию)
with webdriver.Chrome(options=options) as driver:
    print("🚀 Запуск Chrome с новым профилем...")
    print(f"📂 Путь к профилю: {NEW_PROFILE_PATH}")

    # Переход на страницу (блокирует до полной загрузки)
    driver.get(url)
    print(f"📄 Страница: {driver.title}")

    # Начинаем решать
    is_on_task = True
    while True:
        # Идём до страницы с заданием.
        # Если попадаем на страницу с нерешённым заданием, то решаем его.
        # Пытаемся решить задание до тех пор, пока не решим правильно.
        if not next_page(driver):
            task_text = extract_task_text(driver) + "\n\nОшибки:\n" + extract_errors_text(driver)  # Получаем текст задания
            print(task_text)
            answer = complete_task(task_text)  # Получаем ответ от ИИ
            click_try_again_button(driver)  # Нажимаем кнопку "Попробовать снова", если она есть
            time.sleep(0.3)
            insert_code_into_editor(driver, answer)  # Вставляем ответ в форму
            time.sleep(0.3)
            click_send_button(driver)  # Жмём кнопку "Отправить"

            if not check_answer(driver):
                print(f"\n❌   Задание выполнено с ошибкой")
            else:
                print(f"\n✅   Задание выполнено корректно")


        # Если дошли до конца
        if is_end(driver):
            break

    input("⏸️ Нажмите Enter для завершения работы приложения...")
