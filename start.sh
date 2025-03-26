#!/bin/bash

# Оновлення списку пакетів
apt-get update 

# Встановлення Firefox
apt-get install -y firefox

# Завантаження GeckoDriver
GECKODRIVER_VERSION=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d '"' -f 4)
wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz"

# Розпакування GeckoDriver у робочу папку
mkdir -p /opt/firefox/
tar -xzf /tmp/geckodriver.tar.gz -C /opt/firefox/
rm /tmp/geckodriver.tar.gz

# Надаємо права на виконання
chmod +x /opt/firefox/geckodriver

# Запуск бота
python bot.py
