import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Отримуємо токен з перемінних середовища
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv('RENDER_APP_URL'))  # Виправлено
    return 'Webhook set', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ Зв’язок встановлено!\nВи успішно підключені до системи SpaRadarUA.\nОчікуйте повідомлення про нові спа-проєкти.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я отримав твоє повідомлення! 🤖")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
