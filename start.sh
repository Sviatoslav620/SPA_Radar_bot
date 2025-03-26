#!/bin/bash

# Оновлення списку пакетів
apt-get update 

# Встановлення необхідних утиліт
apt-get install -y wget unzip

# Завантаження та встановлення Google Chrome
wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i /tmp/chrome.deb || apt-get install -f -y
rm /tmp/chrome.deb

# Завантаження ChromeDriver
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip

# Розпакування ChromeDriver у робочу папку
unzip /tmp/chromedriver.zip -d /usr/local/bin/
rm /tmp/chromedriver.zip

# Надаємо права на виконання
chmod +x /usr/local/bin/chromedriver

# Запуск бота
python bot.py
