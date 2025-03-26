#!/bin/bash

# Оновлення списку пакетів
apt-get update

# Встановлення необхідних залежностей
apt-get install -y unzip wget

# Завантаження та встановлення Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
dpkg -i chrome.deb || apt-get install -fy
rm chrome.deb

# Завантаження та встановлення ChromeDriver
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -O chromedriver.zip
unzip -o chromedriver.zip -d /usr/local/bin/
rm chromedriver.zip
chmod +x /usr/local/bin/chromedriver

# Запуск бота
python bot.py
