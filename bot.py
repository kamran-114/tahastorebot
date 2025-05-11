import telebot
from flask import Flask, request
import os
import requests
import time

# Tokenlər
TOKEN = "7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Hava məlumatı üçün açar
WEATHER_API_KEY = "8db207e04b11bb5027922faf1eeee944"

# Kitab siyahısı
BOOK_CATALOG = [
    {
        "title": "Müsəlmanlığın əsasları",
        "author": "Əbu Həmid əl-Qəzzali",
        "description": "İslamın təməl prinsiplərini izah edən klassik əsər.",
        "price": "6 AZN"
    },
    {
        "title": "Əl-Kafi (Hədislər toplusu)",
        "author": "Kuleyni",
        "description": "Şiə hədislərinin əsas mənbələrindən biri.",
        "price": "10 AZN"
    },
    {
        "title": "Namazın sirri",
        "author": "Murtəza Mutəhhəri",
        "description": "Namazın mənəvi tərəflərini izah edən dərin əsər.",
        "price": "5 AZN"
    }
]

# Başlanğıc menyu düymələri
from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📚 Kitablar", "🌦️ Hava")
    markup.row("📞 Əlaqə")
    return markup

# Mesaj emalı
@bot.message_handler(func=lambda message: message.text is not None)
def handle_message(message):
    time.sleep(1)
    text = message.text.lower()

    # Salamlaşma cavabları
    if text in ["salam", "salammm", "salam əleykum", "salam aleykum"]:
        bot.reply_to(message, "Əleykum Salam!", reply_markup=main_menu())
    elif "necəsən" in text:
        bot.reply_to(message, "Mən yaxşıyam! Sən necəsən?", reply_markup=main_menu())
    elif any(word in text for word in ["qiymət", "neçəyə"]):
        bot.reply_to(message, "Qiymətlər kitabdan asılı olaraq dəyişir.", reply_markup=main_menu())
    elif any(word in text for word in ["əlaqə", "nömrə"]):
        bot.reply_to(message, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX", reply_markup=main_menu())
    elif any(word in text for word in ["çatdır", "çatdırılma"]):
        bot.reply_to(message, "Çatdırılma Bakıda 1 günə, bölgələrə 2-3 günə çatır.", reply_markup=main_menu())
    elif "📚 kitablar" in text or "kitab" in text:
        query = text.replace("kitab", "").strip()
        msg = search_books(query) if query else "Axtardığınız kitabı adla yaza bilərsiniz."
        bot.reply_to(message, msg, reply_markup=main_menu())
    elif "🌦️ hava" in text or "hava" in text:
        city = text.replace("hava", "").strip()
        msg = get_weather(city) if city else "Zəhmət olmasa şəhər adını daxil edin."
        bot.reply_to(message, msg, reply_markup=main_menu())
    else:
        bot.reply_to(message, "Zəhmət olmasa telefon nömrənizi və ünvanınızı da əlavə edin.", reply_markup=main_menu())

# Hava funksiyası
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=az"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{city.capitalize()} şəhərində hava: {data['weather'][0]['description']}, {data['main']['temp']}°C."
    return "Şəhər tapılmadı və ya hava məlumatı mövcud deyil."

# Kitab axtarışı
def search_books(query):
    query = query.lower()
    results = []
    for book in BOOK_CATALOG:
        if query in book["title"].lower():
            results.append(f"📘 {book['title']}\n✍️ Müəllif: {book['author']}\n📄 {book['description']}\n💰 Qiymət: {book['price']}\n")
    return "\n\n".join(results) if results else "Axtardığınız kitaba uyğun nəticə tapılmadı."

# Flask webhook
@app.route('/')
def index():
    return "Bot işləyir!"

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return 'ok', 200

# Webhooku qur
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://tahastorebot.onrender.com/' + TOKEN)
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

