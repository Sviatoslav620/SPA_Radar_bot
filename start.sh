#!/bin/bash

# Оновлення списку пакетів та встановлення необхідних утиліт
apt-get update && apt-get install -y wget unzip curl

# Встановлення Google Chrome
echo "📥 Завантаження та встановлення Google Chrome..."
wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i /tmp/chrome.deb || apt-get -f install -y
rm /tmp/chrome.deb

# Отримання версії Chrome
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
echo "🚀 Встановлена версія Chrome: $CHROME_VERSION"

# Завантаження відповідного ChromeDriver
echo "📥 Завантаження ChromeDriver..."
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip

# Розпакування ChromeDriver у кореневу папку проекту
unzip /tmp/chromedriver.zip -d /opt/render/project/src/
rm /tmp/chromedriver.zip

# Надаємо права на виконання
chmod +x /opt/render/project/src/chromedriver

# Перевірка встановлення
echo "✅ Перевірка встановлення:"
google-chrome --version
/opt/render/project/src/chromedriver --version

# Запуск бота
echo "🚀 Запуск бота..."
python bot.py
