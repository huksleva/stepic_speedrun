import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# НАСТРОЙКИ
START_URL = "https://example.com/start"  # ВСТАВЬТЕ ВАШУ ССЫЛКУ
TASK_FIELD_SELECTOR = (By.ID, "answer")  # Замените на ваш селектор поля ответа
SUBMIT_BUTTON_SELECTOR = (By.XPATH, "//button[text()='Отправить']")
NEXT_BUTTON_SELECTOR = (By.CSS_SELECTOR, "button.green.next-step")

# Ожидаемый текст успешного выполнения
SUCCESS_TEXT = "Успешно"  # или другой текст / класс / элемент


def do_task(driver, task_element):
    """Здесь выполняется логика для одного задания.
       Например, ввести ответ, выбрать вариант и т.д.
    """

    # Пример: вводим какой-то текст
    task_element.clear()
    task_element.send_keys("Ответ на задание")  # Замените на ваш ответ
    # Если нужны радиокнопки/чекбоксы — обработайте отдельно
    print(driver)


def main():
    # Запуск браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(START_URL)
        print("Страница загружена")

        # Цикл по заданиям (бесконечный, пока есть кнопка "следующий шаг")
        step_number = 1
        while True:
            print(f"\n--- Шаг {step_number} ---")

            # Ждём поле ввода задания (или элемент, указывающий на новое задание)
            try:
                task_input = wait.until(EC.presence_of_element_located(TASK_FIELD_SELECTOR))
            except Exception as e:
                print("Поле задания не найдено. Выходим.")
                print(e)
                break

            # Выполняем действие (заполняем, выбираем)
            do_task(driver, task_input)

            # Жмём "Отправить"
            submit_btn = driver.find_element(*SUBMIT_BUTTON_SELECTOR)
            submit_btn.click()
            print("✓ Отправили ответ")

            # Ждём успешного выполнения (появление элемента "Успешно")
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{SUCCESS_TEXT}')]")))
                print("✓ Задание выполнено успешно")
            except Exception as e:
                print("✗ Не дождались подтверждения успеха. Возможно, сайт выдал ошибку.")
                print(e)
                # Можно сделать скриншот для отладки
                driver.save_screenshot(f"error_step_{step_number}.png")
                break

            # Теперь ищем и жмём кнопку "Следующий шаг" (зелёную)
            try:
                next_btn = wait.until(EC.element_to_be_clickable(NEXT_BUTTON_SELECTOR))
                next_btn.click()
                print("✓ Перешли к следующему шагу")
            except Exception as e:
                print("Кнопка 'Следующий шаг' не найдена или задания кончились.")
                print(e)
                break

            step_number += 1
            time.sleep(1)  # небольшая пауза, чтобы следующий шаг успел прогрузиться

        print("\nВсе шаги выполнены или завершены досрочно.")
        driver.save_screenshot("final_screen.png")

    finally:
        # Закрыть браузер через 5 секунд (чтобы успеть посмотреть)
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()