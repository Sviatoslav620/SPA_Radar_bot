#!/bin/bash

# Надати файлу start.sh права на виконання
chmod +x start.sh

# Завантажуємо Chrome
echo "Downloading Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O chrome.deb
sudo dpkg -i chrome.deb || sudo apt-get -f install -y
rm chrome.deb

# Завантажуємо ChromeDriver
echo "Downloading ChromeDriver..."
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
sudo mv chromedriver /usr/local/bin/
rm chromedriver_linux64.zip

# Запускаємо бота
echo "Starting bot..."
python bot.py
