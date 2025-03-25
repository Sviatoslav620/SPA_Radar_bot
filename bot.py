import os
import time
import random
import requests
import telebot
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from itertools import cycle

# Налаштування змінних середовища
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "@Sviatoslav_Poliakov"
PROXIES = [
    "190.71.174.227:999",
    "43.201.110.79:3128",
    "43.153.119.231:13001",
    "43.153.100.212:13001"
]
proxy_pool = cycle(PROXIES)

# Telegram бот
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Функція для налаштування Webhook
@app.route('/')
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('RENDER_APP_URL')}/{TOKEN}")
    return 'Webhook set', 200

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

# Функція для отримання драйвера з проксі

def get_driver():
    proxy = next(proxy_pool)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--proxy-server=http://{proxy}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver, proxy

# Хештеги та міста
HASHTAGS = [
    "#спа", "#spa", "#сауна", "#баня", "#хамам", "#hamam", "#sauna", "#солянакімната", "#saltroom",
    "#wellness", "#велнес", "#візуалізація", "#3d", "#рендер", "#render", "#visualization",
    "#projectvisualization", "#інтерєр", "#design", "#spacomplex", "#spadesign", "#saunadesign",
    "#spadesigner", "#spaproject", "#hamamdesign"
]

CITIES = ["Київ", "Львів", "Одеса", "Харків", "Дніпро", "Запоріжжя"]

# Функція для парсингу Instagram

def scrape_instagram():
    driver, proxy = get_driver()
    try:
        for hashtag in HASHTAGS:
            url = f"https://www.instagram.com/explore/tags/{hashtag.strip('#')}"  
            driver.get(url)
            time.sleep(random.randint(5, 10))
            
            posts = driver.find_elements(By.CSS_SELECTOR, "article div div div div a")
            for post in posts[:5]:
                link = post.get_attribute("href")
                bot.send_message(CHAT_ID, f"🔍 Знайдено новий пост: {link}")
                time.sleep(random.randint(2, 5))
    
    except Exception as e:
        bot.send_message(CHAT_ID, f"⚠️ Помилка під час парсингу: {e}\nСпробую інший проксі: {proxy}")
    finally:
        driver.quit()

# Обробник команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ Бот запущений! Очікуйте повідомлення про нові спа-проєкти.")

# Запуск Flask-сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
