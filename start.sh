#!/bin/bash

# Встановлення необхідних утиліт
apt-get update && apt-get install -y wget unzip curl

# Завантаження та встановлення Google Chrome
mkdir -p /opt/chrome
wget -O /opt/chrome/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i /opt/chrome/chrome.deb || apt-get install -fy
rm /opt/chrome/chrome.deb

# Завантаження ChromeDriver
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -O /opt/chrome/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip

# Розпакування ChromeDriver у папку
unzip /opt/chrome/chromedriver.zip -d /opt/chrome/
rm /opt/chrome/chromedriver.zip

# Надаємо права на виконання
chmod +x /opt/chrome/chromedriver

# Вказуємо шлях до Chrome та ChromeDriver як змінні середовища
export PATH="/opt/chrome:$PATH"
export CHROME_BIN="/usr/bin/google-chrome"
export CHROMEDRIVER_PATH="/opt/chrome/chromedriver"

# Запуск бота
python bot.py
