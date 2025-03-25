#!/bin/bash

# Завантаження Chrome
apt-get update
apt-get install -y wget unzip
wget -q -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./chrome.deb
rm chrome.deb

# Завантаження ChromeDriver (під версію Chrome)
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -q -O chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver.zip -d /usr/local/bin/
rm chromedriver.zip

# Запуск бота
python3 bot.py
