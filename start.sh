#!/bin/bash

# Оновлення списку пакетів
apt-get update -y 

# Встановлення необхідних утиліт
apt-get install -y wget unzip curl

# Завантаження та встановлення Google Chrome
wget -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i /tmp/chrome.deb || apt-get -f install -y  # Виправлення залежностей, якщо потрібно
rm /tmp/chrome.deb

# Переконуємося, що Chrome встановлено
if ! command -v google-chrome &> /dev/null; then
    echo "Помилка: Google Chrome не встановлено!"
    exit 1
fi

# Завантаження ChromeDriver
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip

# Розпакування ChromeDriver у систему
unzip /tmp/chromedriver.zip -d /usr/bin/
rm /tmp/chromedriver.zip

# Надаємо права на виконання
chmod +x /usr/bin/chromedriver

# Виведення версій Chrome та ChromeDriver для перевірки
google-chrome --version
chromedriver --version

# Запуск бота
python bot.py
