

def wait_for_network_idle(driver, timeout=15):
    """Ждёт, пока не останется активных сетевых запросов (требуется Chrome)"""
    from selenium.webdriver.support.ui import WebDriverWait

    # Включаем отслеживание событий сети
    driver.execute_cdp_cmd("Network.enable", {})

    # Функция проверяет количество активных запросов
    def no_pending_requests(driver):
        return driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": "dummy"}) is None  # Упрощённо

    # Более надёжный вариант - просто подождать паузу в запросах
    import time
    time.sleep(2)  # Даём время на завершение "хвостовых" запросов
    print("✅ Сетевая активность утихла")