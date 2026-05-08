import shutil
from pathlib import Path
from dotenv import load_dotenv
import os
import subprocess
import platform

load_dotenv()

# ВНИМАНИЕ
# ФАЙЛ ПРЕДНАЗНАЧЕН ТОЛЬКО ДЛЯ РУЧНОГО ИСПОЛЬЗОВАНИЯ

# Путь к НОВОМУ профилю (создастся автоматически при первом запуске)
PROFILE_DIR_NAME = "SeleniumProfile"
NEW_PROFILE_PATH = str(os.environ.get("CHROME_PROFILE_PATH")) + PROFILE_DIR_NAME


def delete_profile():
    """Удаление папки с профилем"""

    try:
        folder = Path(NEW_PROFILE_PATH)
        shutil.rmtree(folder)
        print("✅ Папка", folder, "успешно удалена")
    except Exception as e:
        print("Папка уже удалена")
        print(e)

def kill_all_chrome():
    """Завершает все процессы chrome browser"""

    if platform.system() == "Windows":
        cmd = ["taskkill", "/F", "/IM", "chrome.exe"]
    else:  # Linux/macOS
        cmd = ["pkill", "-9", "chrome"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Все процессы Chrome завершены")
    except Exception as e:
        print(f"❌ Ошибка: {e}")



