import os
import telebot
import requests
import time
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Отримання змінних середовища
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_APP_URL = "https://spa-radar-bot.onrender.com"
CHAT_ID = "@Sviatoslav_Poliakov"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Проксі-сервери
PROXIES = [
    "190.71.174.227:999",
    "43.201.110.79:3128",
    "43.153.119.231:13001",
    "43.153.100.212:13001"
]

# Хештеги для пошуку
HASHTAGS = [
    "#спа", "#spa", "#сауна", "#баня", "#хамам", "#hamam", "#sauna",
    "#солянакімната", "#saltroom", "#wellness", "#велнес", "#візуалізація",
    "#3d", "#рендер", "#render", "#visualization", "#projectvisualization",
    "#інтерєр", "#design", "#spacomplex", "#spadesign", "#saunadesign",
    "#spadesigner", "#spaproject", "#hamamdesign"
]

# Налаштовуємо Selenium
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск у фоновому режимі
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Використовуємо проксі
    proxy = PROXIES.pop(0)  # Беремо перший проксі
    PROXIES.append(proxy)  # Переміщаємо в кінець черги
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# Функція парсингу Instagram
def scrape_instagram():
    try:
        driver = get_driver()
        driver.get("https://www.instagram.com/explore/tags/spa/")  # Приклад для парсингу за хештегом
        
        time.sleep(5)  # Чекаємо завантаження сторінки
        
        posts = driver.find_elements("css selector", "article a")  # Пошук публікацій
        
        for post in posts[:5]:  # Беремо перші 5 постів
            link = post.get_attribute("href")
            bot.send_message(CHAT_ID, f"🔍 Знайдено новий пост: {link}")
        
        driver.quit()
    except Exception as e:
        bot.send_message(CHAT_ID, f"⚠️ Помилка під час парсингу: {e}")

# Обробник webhook
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_APP_URL}/{TOKEN}")
    return 'Webhook set', 200

# Обробник команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ Зв’язок встановлено!\nВи успішно підключені до системи SpaRadarUA.\nОчікуйте повідомлення про нові спа-проєкти.")

# Перевірка блокування
def check_if_banned():
    try:
        bot.send_message(CHAT_ID, "🛠 Бот працює нормально.")
    except Exception as e:
        bot.send_message(CHAT_ID, f"⚠️ Бот, можливо, заблокований! Помилка: {e}")

if __name__ == "__main__":
    check_if_banned()
    scrape_instagram()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


