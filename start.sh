#!/bin/bash

# Оновлення списку пакетів та встановлення необхідних утиліт
apt-get update
apt-get install -y wget tar unzip curl jq

# Встановлення Firefox
echo "🔵 Завантаження та встановлення Firefox..."
wget -O /tmp/firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"
mkdir -p /opt/firefox
tar -xjf /tmp/firefox.tar.bz2 -C /opt/firefox
rm /tmp/firefox.tar.bz2
ln -sf /opt/firefox/firefox /usr/local/bin/firefox

# Встановлення GeckoDriver
echo "🟢 Завантаження та встановлення GeckoDriver..."
GECKODRIVER_VERSION=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r ".tag_name" | sed 's/v//')
wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-linux64.tar.gz"
mkdir -p /opt/geckodriver
tar -xzf /tmp/geckodriver.tar.gz -C /opt/geckodriver
rm /tmp/geckodriver.tar.gz
chmod +x /opt/geckodriver/geckodriver
ln -sf /opt/geckodriver/geckodriver /usr/local/bin/geckodriver

# Перевірка встановлення
echo "✅ Firefox версія:"
firefox --version
echo "✅ GeckoDriver версія:"
geckodriver --version

# Запуск бота
python bot.py
