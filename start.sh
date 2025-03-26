#!/bin/bash

echo "🔄 Оновлення списку пакетів..."
apt-get update 

echo "📦 Встановлення залежностей..."
apt-get install -y wget unzip curl

echo "🌍 Завантаження та встановлення Google Chrome..."
wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i /tmp/chrome.deb || apt-get install -fy
rm /tmp/chrome.deb

echo "📥 Завантаження ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)
wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip

echo "📂 Розпакування ChromeDriver..."
unzip /tmp/chromedriver.zip -d /usr/local/bin/
rm /tmp/chromedriver.zip
chmod +x /usr/local/bin/chromedriver

echo "🛠 Перевірка встановленого ChromeDriver..."
if [ ! -f "/usr/local/bin/chromedriver" ]; then
    echo "❌ ПОМИЛКА: ChromeDriver не було встановлено!"
    exit 1
fi

echo "🐍 Встановлення Python-залежностей..."
pip install --no-cache-dir -r requirements.txt

echo "🚀 Запуск бота..."
python bot.py
