#!/bin/bash

# Оновлення списку пакетів
apt-get update

# Завантаження та встановлення Firefox у доступну папку
mkdir -p /tmp/firefox
wget -O /tmp/firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"
tar xjf /tmp/firefox.tar.bz2 -C /tmp/firefox
rm /tmp/firefox.tar.bz2
export PATH="/tmp/firefox/firefox/:$PATH"

# Завантаження та встановлення Geckodriver
GECKODRIVER_VERSION=$(curl -sS https://github.com/mozilla/geckodriver/releases/latest | grep -oP 'v\d+\.\d+\.\d+')
wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-linux64.tar.gz"
tar -xzf /tmp/geckodriver.tar.gz -C /tmp/firefox/
rm /tmp/geckodriver.tar.gz
chmod +x /tmp/firefox/geckodriver
export PATH="/tmp/firefox/:$PATH"

# Логування версій для перевірки
echo "Firefox version:"
/tmp/firefox/firefox --version

echo "Geckodriver version:"
/tmp/firefox/geckodriver --version

# Запуск бота
python bot.py
