from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_end(driver, timeout=0.5):
    """Проверяет, находится ли на последней странице курса (появилось модальное окно завершения)"""

    try:
        # Ищем модальное окно завершения курса (ждем до 1 секунд)
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".modal-popup__container"
        )))

        print("✅ Курс завершён! Найдено модальное окно.")
        return True

    except TimeoutException:
        # Элемент не найден — значит ещё есть шаги
        return False
    except Exception as e:
        print("Ошибка:", e)
        return False