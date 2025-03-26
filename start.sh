#!/bin/bash

# Встановлення необхідних утиліт
wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
mkdir -p /tmp/chrome
dpkg-deb -x /tmp/chrome.deb /tmp/chrome
export PATH="/tmp/chrome/usr/bin:$PATH"

# Завантаження ChromeDriver
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip

# Розпакування ChromeDriver
unzip /tmp/chromedriver.zip -d /tmp/
chmod +x /tmp/chromedriver
export PATH="/tmp:$PATH"

# Запуск бота
python bot.py
