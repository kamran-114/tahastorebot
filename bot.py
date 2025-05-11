import telebot
from flask import Flask, request
import os
import requests

# Tokenlər
TOKEN = "7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Hava məlumatı üçün açar
WEATHER_API_KEY = "8db207e04b11bb5027922faf1eeee944"

# Dini Kitablar kataloqu
BOOK_CATALOG = {
    "Dini Kitablar": {
        "Hədislər": [
            {
                "title": "Əl-Kafi (Hədislər toplusu)",
                "author": "Kuleyni",
                "description": "Şiə hədislərinin əsas mənbələrindən biri.",
                "price": "10 AZN"
            },
            {
                "title": "Geybəti Numani",
                "author": "Numani",
                "description": "Əhli-beyt ilə əlaqəli qiymətli hədislər.",
                "price": "8 AZN"
            }
        ],
        "Namaz Kitabları": [
            {
                "title": "Namazın sirri",
                "author": "Murtəza Mutəhhəri",
                "description": "Namazın mənəvi tərəflərini izah edən dərin əsər.",
                "price": "5 AZN"
            },
            {
                "title": "Namaz və Hədislər",
                "author": "İmam Cəfər Sadiq",
                "description": "Namaz və onun dini mənası haqqında geniş məlumat.",
                "price": "7 AZN"
            }
        ]
    }
}

# İstifadəçi mesajlarını emal edən funksiya
@bot.message_handler(func=lambda message: message.text is not None)
def handle_message(message):
    text = message.text.lower()

    if "dini kitablar" in text:
        msg = "Dini Kitablar mövzusuna xoş gəlmisiniz! Aşağıdakı bölmələrdən birini seçin:\n"
        msg += "1. Hədislər\n2. Namaz Kitabları\n\nZəhmət olmasa seçim edin."
        bot.reply_to(message, msg)

    elif "hədislər" in text:
        msg = "Hədislər kitabları:\n"
        for book in BOOK_CATALOG["Dini Kitablar"]["Hədislər"]:
            msg += f"📘 {book['title']}\n✍️ Müəllif: {book['author']}\n📄 {book['description']}\n💰 Qiymət: {book['price']}\n\n"
        bot.reply_to(message, msg)

    elif "namaz kitabları" in text:
        msg = "Namaz kitabları:\n"
        for book in BOOK_CATALOG["Dini Kitablar"]["Namaz Kitabları"]:
            msg += f"📘 {book['title']}\n✍️ Müəllif: {book['author']}\n📄 {book['description']}\n💰 Qiymət: {book['price']}\n\n"
        bot.reply_to(message, msg)

    else:
        bot.reply_to(message, "Zəhmət olmasa, mövzu seçin: 'Dini Kitablar'")

# Hava məlumatını çəkən funksiya
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=az"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{city.capitalize()} şəhərində hava: {data['weather'][0]['description']}, {data['main']['temp']}°C."
    return "Şəhər tapılmadı və ya hava məlumatı mövcud deyil."

# Flask interfeysi (webhook üçün)
@app.route('/')

def index():
    return "Bot işləyir!"

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return 'ok', 200

# Əsas işlədici hissə
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://tahastorebot.onrender.com/' + TOKEN)

    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
