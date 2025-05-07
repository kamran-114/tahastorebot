import telebot
from flask import Flask, request
import os
import threading

# TOKEN burada təyin olunur
TOKEN = "7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI"
bot = telebot.TeleBot(TOKEN)

# Mesaj cavabları
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    if "kitab" in text:
        bot.reply_to(message, "Hansı janrda kitab axtarırsınız?")
    elif "qiymət" in text:
        bot.reply_to(message, "Qiymətlər kitabdan asılı olaraq dəyişir.")
    elif "əlaqə" in text or "nömrə" in text:
        bot.reply_to(message, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    else:
        bot.reply_to(message, "Zəhmət olmasa telefon nömrənizi və ünvanınızı da əlavə edin.")

# Flask tətbiqi
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot işləyir!"

# Telebot-u paralel işlətmək üçün
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
