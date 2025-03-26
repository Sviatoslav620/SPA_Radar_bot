import os
import json
import time
import random
import telebot
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Отримуємо токен з перемінних середовища
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

USERS_FILE = "users.json"
PROXIES = [
    "190.71.174.227:999",
    "43.201.110.79:3128",
    "43.153.119.231:13001",
    "43.153.100.212:13001"
]

HASHTAGS = [
    "спа", "spa", "сауна", "баня", "хамам", "hamam", "sauna", "солянакімната", "saltroom",
    "wellness", "велнес", "візуалізація", "3d", "рендер", "render", "visualization", "projectvisualization",
    "інтерєр", "design", "spacomplex", "spadesign", "saunadesign", "spadesigner", "spaproject", "hamamdesign"
]


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


def send_message_to_all_users(text):
    users = load_users()
    for user_id in users:
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"Помилка надсилання повідомлення {user_id}: {e}")


def get_random_proxy():
    return random.choice(PROXIES)


def scrape_instagram():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--proxy-server={get_random_proxy()}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://www.instagram.com/explore/tags/spa/")
        time.sleep(5)
        posts = driver.find_elements(By.CSS_SELECTOR, "article div a")
        for post in posts[:5]:
            link = post.get_attribute("href")
            send_message_to_all_users(f"🔔 Знайдено новий пост: {link}")
    except Exception as e:
        print(f"Помилка парсингу Instagram: {e}")
    finally:
        driver.quit()


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://spa-radar-bot.onrender.com/{TOKEN}")
    return 'Webhook set', 200


@bot.message_handler(commands=['start'])
def send_welcome(message):
    users = load_users()
    user_id = message.chat.id
    if user_id not in users:
        users.append(user_id)
        save_users(users)
    bot.reply_to(message, "✅ Зв’язок встановлено!\nВи успішно підключені до системи SpaRadarUA.\nОчікуйте повідомлення про нові спа-проєкти.")


@bot.message_handler(commands=['check'])
def check_instagram(message):
    bot.reply_to(message, "🔍 Шукаю нові пости...")
    scrape_instagram()
    bot.reply_to(message, "✅ Оновлення завершено!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
