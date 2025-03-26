import os
import json
import time
import logging
import random
import telebot
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Логування для налагодження
logging.basicConfig(level=logging.INFO)

# Завантаження змінних середовища
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = f"https://spa-radar-bot.onrender.com/{TOKEN}"
PORT = int(os.getenv("PORT", 5000))

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Файл для збереження користувачів
USERS_FILE = "instance/users.json"

# Перелік хештегів для моніторингу
HASHTAGS = [
    "#спа", "#spa", "#сауна", "#баня", "#хамам", "#hamam", "#sauna", "#солянакімната",
    "#saltroom", "#wellness", "#велнес", "#візуалізація", "#3d", "#рендер", "#render",
    "#visualization", "#projectvisualization", "#інтерєр", "#design", "#spacomplex",
    "#spadesign", "#saunadesign", "#spadesigner", "#spaproject", "#hamamdesign"
]

# Створення директорії, якщо її немає
if not os.path.exists("instance"):
    os.makedirs("instance")

# Завантаження списку користувачів
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return []

# Збереження списку користувачів
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

users = load_users()

# Налаштування Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/opt/render/project/src/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Маршрути Flask
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route("/")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return 'Webhook set', 200

# Обробник команди /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    if user_id not in users:
        users.append(user_id)
        save_users(users)

    bot.send_message(user_id, "✅ Вітаю! Ти підписався на оновлення про SPA, сауни та релакс-зони в Україні!")

# Функція парсингу постів з Instagram
def scrape_instagram():
    global users
    try:
        logging.info("🔍 Перевіряємо Instagram...")
        driver.get("https://www.instagram.com/explore/tags/spa/")
        time.sleep(random.randint(3, 6))  # Час очікування, щоб зменшити ризик блокування

        posts = driver.find_elements(By.XPATH, "//article//a")
        found_posts = []

        for post in posts[:5]:  # Перевіряємо перші 5 постів
            link = post.get_attribute("href")
            if any(tag in link for tag in HASHTAGS):
                found_posts.append(link)

        if found_posts:
            message = "🆕 Нові пости з Instagram:\n" + "\n".join(found_posts)
            for user_id in users:
                try:
                    bot.send_message(user_id, message)
                except Exception as e:
                    logging.error(f"Не вдалося відправити повідомлення {user_id}: {e}")

    except Exception as e:
        logging.error(f"Помилка при парсингу: {e}")

# Функція періодичної перевірки постів
def check_new_posts():
    while True:
        scrape_instagram()
        time.sleep(1800)  # Чекати 30 хвилин перед наступною перевіркою

# Запуск сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
