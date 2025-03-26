#!/bin/bash

echo "📥 Завантаження Portable Google Chrome..."
wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -x /tmp/chrome.deb /tmp/chrome
rm /tmp/chrome.deb

echo "📥 Завантаження ChromeDriver..."
CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip

echo "📂 Розпакування ChromeDriver..."
unzip /tmp/chromedriver.zip -d /tmp/
rm /tmp/chromedriver.zip
chmod +x /tmp/chromedriver

echo "🔧 Додавання Chrome в PATH..."
export PATH="/tmp/chrome/usr/bin:$PATH"
export PATH="/tmp:$PATH"

echo "🛠 Перевірка встановленого ChromeDriver..."
if [ ! -f "/tmp/chromedriver" ]; then
    echo "❌ ПОМИЛКА: ChromeDriver не було встановлено!"
    exit 1
fi

echo "🐍 Встановлення Python-залежностей..."
pip install --no-cache-dir -r requirements.txt

echo "🚀 Запуск бота..."
python bot.py
