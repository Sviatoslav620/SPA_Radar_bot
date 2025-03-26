#!/bin/bash

echo "📥 Завантаження Google Chrome..."
wget -q -O /tmp/chrome.tar.gz https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
mkdir -p /opt/chrome
tar -xzf /tmp/chrome.tar.gz -C /opt/chrome
rm /tmp/chrome.tar.gz

echo "📥 Завантаження ChromeDriver..."
CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip

echo "📂 Розпакування ChromeDriver..."
unzip /tmp/chromedriver.zip -d /opt/chrome/
rm /tmp/chromedriver.zip
chmod +x /opt/chrome/chromedriver

echo "🛠 Перевірка встановленого ChromeDriver..."
if [ ! -f "/opt/chrome/chromedriver" ]; then
    echo "❌ ПОМИЛКА: ChromeDriver не було встановлено!"
    exit 1
fi

echo "🐍 Встановлення Python-залежностей..."
pip install --no-cache-dir -r requirements.txt

echo "🚀 Запуск бота..."
python bot.py
