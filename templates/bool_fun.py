from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_end(driver):
    """Проверяет, находится ли на последней странице курса"""

    try:


        return True
    except Exception as e:
        print("Ошибка:", e)
        return False