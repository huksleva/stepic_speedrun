FROM python:3.11-bookworm

# Устанавливаем зависимости для Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    curl \
    unzip \
    libxss1 \
    libappindicator3-1 \
    libnss3 \
    libglib2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libgtk-3-0 \
    fonts-liberation \
    fonts-noto-color-emoji \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ❌ УДАЛЯЕМ ручную установку ChromeDriver — Selenium Manager сделает это сам!

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Переменные окружения
ENV CHROME_HEADLESS=true
ENV PYTHONUNBUFFERED=1
# Важно для Selenium Manager в Docker:
ENV SE_MANAGER_LOG_LEVEL=ERROR

# Запуск
CMD ["python", "main.py"]