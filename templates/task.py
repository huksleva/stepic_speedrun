from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
from pprint import pprint


# НАСТРОЙКА ПОДКЛЮЧЕНИЯ К ИИ
url = "https://api.intelligence.io.solutions/api/v1/models?page=1&page_size=50"
api_key = str(os.getenv("API_KEY"))
headers = {"Authorization": "Bearer " + api_key}
response = requests.get(url, headers=headers)
print(response.text)


def get_task(driver):

    pass

def complete_task(driver):
    pass

