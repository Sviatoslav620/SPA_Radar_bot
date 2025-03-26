#!/bin/bash

# Оновлення списку пакетів та встановлення необхідних утиліт
apt-get update && apt-get install -y wget unzip curl

# Встановлення Google Chrome
echo "📥 Завантаження та встановлення Google Chrome..."
wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i /tmp/chrome.deb || apt-get -f install -y
rm /tmp/chrome.deb

# Отримання версії ChromeDriver, яка відповідає встановленому Chrome
echo "📥 Завантаження ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip

# Розпакування ChromeDriver у робочу папку
unzip /tmp/chromedriver.zip -d /usr/local/bin/
rm /tmp/chromedriver.zip

# Надаємо права на виконання
chmod +x /usr/local/bin/chromedriver

# Перевірка встановлення
echo "✅ Перевірка встановлення:"
google-chrome --version
chromedriver --version

# Запуск бота
echo "🚀 Запуск бота..."
python bot.py
