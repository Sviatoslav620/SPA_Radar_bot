import os
import time
import random
import requests
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ---------- Налаштування ----------
TELEGRAM_BOT_TOKEN = "7928931611:AAGDiej_au6ODeB1bGfTV3wVp1ayLD_iU8U"
CHAT_ID = "@Sviatoslav_Poliakov"
PROXIES = [
    "190.71.174.227:999",
    "43.201.110.79:3128",
    "43.153.119.231:13001",
    "43.153.100.212:13001"
]
HASHTAGS = ["#спа", "#spa", "#сауна", "#баня", "#хамам", "#hamam", "#sauna", "#солянакімната", "#saltroom", "#wellness", "#велнес", "#візуалізація", "#3d", "#рендер", "#render", "#visualization", "#projectvisualization", "#інтерєр", "#design", "#spacomplex", "#spadesign", "#saunadesign", "#spadesigner", "#spaproject", "#hamamdesign"]
CITIES = ["Київ", "Львів", "Одеса", "Дніпро", "Харків", "Запоріжжя"]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ---------- Функція для відправки повідомлень в Telegram ----------
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# ---------- Функція для запуску Selenium з проксі ----------
def get_driver(proxy=None):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# ---------- Основна функція ----------
def scrape_instagram():
    for proxy in PROXIES:
        try:
            driver = get_driver(proxy)
            send_telegram_message(f"🔍 Використовую проксі: {proxy}")
            
            for hashtag in HASHTAGS:
                url = f"https://www.instagram.com/explore/tags/{hashtag[1:]}/"
                driver.get(url)
                time.sleep(random.uniform(5, 10))
                
                posts = driver.find_elements(By.CLASS_NAME, "_aagw")
                
                for post in posts[:5]:  # Аналізуємо перші 5 постів
                    try:
                        post.click()
                        time.sleep(3)
                        
                        location = driver.find_element(By.CLASS_NAME, "_a6hd").text
                        
                        if any(city in location for city in CITIES):
                            post_link = driver.current_url
                            send_telegram_message(f"📍 Новий пост з {location}: {post_link}")
                        
                    except Exception as e:
                        print("Помилка аналізу поста:", e)
                        
            driver.quit()
            break  # Якщо проксі працює – виходимо
        
        except Exception as e:
            send_telegram_message(f"⚠️ Проксі {proxy} не працює. Помилка: {e}")
            driver.quit()

    send_telegram_message("❌ Усі проксі заблоковані! Бот зупинено.")

# ---------- Запускаємо ----------
if __name__ == "__main__":
    send_telegram_message("🚀 Бот запущено!")
    while True:
        scrape_instagram()
        time.sleep(3600)  # Парсимо раз на годину
