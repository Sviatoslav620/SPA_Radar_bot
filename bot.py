import os
import time
import random
import requests
import telebot
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Отримання даних з Environment Variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_APP_URL = os.getenv("RENDER_APP_URL")
PORT = int(os.getenv("PORT", 5000))
CHAT_ID = "@Sviatoslav_Poliakov"  # ID твого Телеграму

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Список українських міст (щоб шукати локацію)
UKRAINE_CITIES = ["Київ", "Львів", "Одеса", "Дніпро", "Харків", "Запоріжжя", "Вінниця", "Чернігів"]

# Хештеги для пошуку
HASHTAGS = [
    "спа", "spa", "сауна", "баня", "хамам", "hamam", "sauna", "солянакімната", "saltroom",
    "wellness", "велнес", "візуалізація", "3d", "рендер", "render", "visualization",
    "projectvisualization", "інтерєр", "design", "spacomplex", "spadesign", "saunadesign",
    "spadesigner", "spaproject", "hamamdesign"
]

# Проксі-сервери (випадковий вибір)
PROXIES = [
    "190.71.174.227:999",
    "43.201.110.79:3128",
    "43.153.119.231:13001",
    "43.153.100.212:13001"
]

def get_proxy():
    """Функція вибору випадкового проксі."""
    return random.choice(PROXIES)

def scrape_instagram():
    """Парсинг постів в Instagram із Selenium."""
    driver = None  # Глобально ініціалізуємо driver, щоб уникнути помилки

    try:
        # Налаштування проксі
        proxy = get_proxy()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Запуск без графічного інтерфейсу
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--proxy-server=http://{proxy}")

        # Запускаємо WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Перебираємо хештеги
        for tag in HASHTAGS:
            url = f"https://www.instagram.com/explore/tags/{tag}/"
            driver.get(url)
            time.sleep(5)  # Чекаємо, поки сторінка завантажиться

            posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")[:5]  # Беремо перші 5 постів
            for post in posts:
                link = post.get_attribute("href")

                # Шукаємо місто в описі
                description = post.text.lower()
                location = next((city for city in UKRAINE_CITIES if city.lower() in description), "Невідоме місто")

                # Надсилаємо повідомлення в Телеграм
                bot.send_message(CHAT_ID, f"📢 Новий пост з тегом #{tag}\n📍 Локація: {location}\n🔗 Посилання: {link}")
        
        return "Парсинг завершено!", 200

    except Exception as e:
        print(f"❌ Помилка парсингу: {e}")
        bot.send_message(CHAT_ID, f"⚠️ ПОМИЛКА ПРИ ПАРСИНГУ: {e}")

    finally:
        if driver:
            driver.quit()  # Закриваємо WebDriver

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    """Обробка оновлень від Telegram API."""
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    """Перевстановлення Webhook для Telegram."""
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{RENDER_APP_URL}/{TOKEN}")
    return 'Webhook set', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Привітальне повідомлення."""
    bot.reply_to(message, "✅ Бот підключений! Я буду відслідковувати нові спа-проекти в Україні.")

@bot.message_handler(commands=['check'])
def check_instagram(message):
    """Команда для ручного запуску парсингу."""
    bot.reply_to(message, "🔍 Починаю пошук нових спа-проєктів...")
    scrape_instagram()

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Відповідає на будь-яке повідомлення."""
    bot.reply_to(message, "Я отримав твоє повідомлення! 🤖")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
