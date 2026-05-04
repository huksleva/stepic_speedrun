import subprocess
import time
from selenium import webdriver


def kill_chrome_background():
    """Убивает ВСЕ процессы Chrome, включая фоновые"""
    for proc in ["chrome.exe", "chromedriver.exe"]:
        try:
            subprocess.run(["taskkill", "/F", "/IM", proc],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        except:
            pass
    time.sleep(2)  # Ждём, пока Windows снимет блокировки с файлов профиля


# 1. Чистим процессы перед запуском
kill_chrome_background()

USER_DATA_DIR = r"C:\Users\Leonid\AppData\Local\Google\Chrome\User Data"
PROFILE_DIR = "Default"

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
options.add_argument(f"--profile-directory={PROFILE_DIR}")

# 🚫 Убрали конфликтные флаги (--remote-debugging-port, --no-sandbox и т.д.)
# ✅ Оставили только необходимое для стабильности на Windows
options.add_argument("--disable-background-networking")
options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-backgrounding-occluded-windows")
options.add_argument("--disable-renderer-backgrounding")

# Скрытие признаков автоматизации
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

print("🚀 Запуск Chrome с вашим профилем...")
try:
    driver = webdriver.Chrome(options=options)
    print("✅ Браузер успешно запущен!")

    driver.get("https://stepik.org/lesson/297514/step/6?unit=279274")
    print(f"📄 Заголовок: {driver.title}")

    input("⏸️ Нажмите Enter для закрытия браузера...")

except Exception as e:
    print(f"❌ Ошибка: {type(e).__name__}: {e}")
finally:
    if 'driver' in locals():
        driver.quit()
        print("🔒 Браузер закрыт")