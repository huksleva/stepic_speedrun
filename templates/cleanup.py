import subprocess
import os

print("🧹 Завершение всех процессов Chrome...")
subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'])

print("🧹 Завершение процессов chromedriver...")
subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'])

print("✅ Очистка завершена!")
input("Нажмите Enter...")