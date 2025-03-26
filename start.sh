#!/bin/bash

# Оновлення списку пакетів
apt-get update

# Встановлення необхідних утиліт
apt-get install -y wget tar unzip

# Завантаження та встановлення Firefox
wget -O /tmp/firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"
tar xjf /tmp/firefox.tar.bz2 -C /opt/
ln -s /opt/firefox/firefox /usr/local/bin/firefox
rm /tmp/firefox.tar.bz2

# Завантаження та встановлення GeckoDriver
GECKODRIVER_VERSION=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d '"' -f 4 | sed 's/v//')
wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz"
tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin/
chmod +x /usr/local/bin/geckodriver
rm /tmp/geckodriver.tar.gz

# Запуск бота
python bot.py
