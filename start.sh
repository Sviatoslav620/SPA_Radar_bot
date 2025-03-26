#!/bin/bash

# Оновлення пакетів
apt-get update
apt-get install -y wget tar unzip curl jq

# Створюємо робочі директорії в домашній папці
mkdir -p ~/firefox
mkdir -p ~/geckodriver

# Встановлення Firefox
echo "🔵 Завантаження та встановлення Firefox..."
wget -O ~/firefox/firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"
tar -xjf ~/firefox/firefox.tar.bz2 -C ~/firefox
rm ~/firefox/firefox.tar.bz2

# Додаємо Firefox у PATH
export PATH=$HOME/firefox:$PATH

# Встановлення GeckoDriver
echo "🟢 Завантаження та встановлення GeckoDriver..."
GECKODRIVER_VERSION="0.33.0"
wget -O ~/geckodriver/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-linux64.tar.gz"

# Перевіряємо, чи файл існує
if [ ! -f "~/geckodriver/geckodriver.tar.gz" ]; then
    echo "❌ Помилка: Файл geckodriver.tar.gz не завантажився!"
    exit 1
fi

tar -xzf ~/geckodriver/geckodriver.tar.gz -C ~/geckodriver
rm ~/geckodriver/geckodriver.tar.gz
chmod +x ~/geckodriver/geckodriver

# Додаємо GeckoDriver у PATH
export PATH=$HOME/geckodriver:$PATH

# Перевірка версій
echo "✅ Firefox версія:"
firefox --version || echo "❌ Firefox не знайдено!"
echo "✅ GeckoDriver версія:"
geckodriver --version || echo "❌ GeckoDriver не знайдено!"

# Запуск бота
python bot.py
