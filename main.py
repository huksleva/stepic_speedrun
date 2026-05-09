from selenium import webdriver
import os
from templates.enter_next_page import next_page, next_button_element
from templates.task import (
    extract_task_text,
    complete_task,
    insert_code_into_editor,
    click_send_button,
    click_try_again_button,
    check_answer,
    extract_errors_text,
    extract_all_images,
    extract_comments_text,
    show_system_alert,
    show_system_alert_nonblocking
)
from templates.clean import kill_all_chrome
from templates.bool_fun import is_end
from dotenv import load_dotenv
from pathlib import Path
import time
from random import uniform

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
with (webdriver.Chrome(options=options) as driver):
    print("🚀 Запуск Chrome с новым профилем...")
    print("📄 ТЕСТЫ на Cтепике нужно проходить в ручном режиме")
    print(f"📂 Путь к профилю: {NEW_PROFILE_PATH}")

    # Переход на страницу (блокирует до полной загрузки)
    driver.get(url)
    print(f"📄 Страница: {driver.title}")

    # Начинаем решать
    err_count = 0 # Счётчик неправильных ответов на одно задание
    while True:
        # Если неправильных ответов больше 5, то
        # рекомендуется решить задание вручную
        if err_count > 4:
            # show_system_alert("Ошибка ИИ", "На это задание потрачено >5 попыток. Рекомендуется решить вручную.")
            # exit(0)
            print("На это задание потрачено уже 5 попыток. Рекомендуется решить вручную.")
            next_btn = next_button_element(driver)
            next_btn.click()
            err_count = 0
            print("Переход к следующему заданию")


        # Идём до страницы с заданием.
        # Если попадаем на страницу с нерешённым заданием, то решаем его.
        # Пытаемся решить задание до тех пор, пока не решим правильно.
        if not next_page(driver):
            # Текст
            print("ИЗВЛЕЧЕНИЕ ИНФОРМАЦИИ СО СТРАНИЦЫ")
            # Если пытаемся решить задание 1-й раз
            if err_count == 0:
                task_text = extract_task_text(driver) + extract_errors_text(driver)
                task_text += extract_comments_text(driver)[:1000]  # Ограничение по кол-ву символов для комментариев
            # Если пытаемся уже не в первый раз
            else:
                task_text = extract_errors_text(driver) + extract_comments_text(driver)[:10000]
            #print(task_text)

            # Изображения
            print("ИЗВЛЕЧЕНИЕ ИЗОБРАЖЕНИЙ СО СТРАНИЦЫ")
            imgs = extract_all_images(driver)

            # Отправляем текст и изображения
            print("ОТПРАВКА ТЕКСТА И ИЗОБРАЖЕНИЙ ИИ")
            answer = complete_task(task_text, imgs)

            # Остальная логика
            click_try_again_button(driver)
            time.sleep(uniform(0.11, 0.21)) # Рандомизация задержки для усложнения отслеживания программы сайтом
            insert_code_into_editor(driver, answer)
            time.sleep(uniform(0.11, 0.21))
            click_send_button(driver)

            if not check_answer(driver):
                print(f"\n❌   Задание выполнено с ошибкой")
                err_count += 1
            else:
                print(f"\n✅   Задание выполнено корректно")
                err_count = 0


        # Если дошли до конца
        print("ПРОВЕРКА КОНЕЦ ИЛИ НЕТ")
        if is_end(driver):
            print("✅✅✅Программа прошла весь курс до конца✅✅✅")
            break
        print("ПРОВЕРКА ЗАВЕРШЕНА")

    input("⏸️ Нажмите Enter для завершения работы приложения...")
