import os
import telebot
from flask import Flask

# Telegram botunun tokenini daxil et
bot = telebot.TeleBot("YOUR_BOT_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

# Telegram botunun mətnləri ilə işləyən hissə
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if "kitab" in text:
        bot.reply_to(message, "Hansı janrda kitab axtarırsınız?")
    elif "qiymət" in text:
        bot.reply_to(message, "Qiymətlər kitabdan asılı olaraq dəyişir.")
    elif "əlaqə" in text or "nömrə" in text:
        bot.reply_to(message, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    else:
        bot.reply_to(message, "Zəhmət olmasa telefon nömrənizi və ünvanınızı da əlavə edin.")

# Flask serverini işə salmaq üçün
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port)

    # Telegram botu üçün polling
    bot.infinity_polling()

