import telebot
from flask import Flask, request
import os
import requests
import time
from telebot import types

TOKEN = "7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

WEATHER_API_KEY = "8db207e04b11bb5027922faf1eeee944"

BOOK_CATALOG = [
    {
        "title": "14 Məsumun(s) həyatı",
        "author": "Ayətullah Müdərrisi",
        "description": "Məsumların həyatı haqqında kitab.",
        "price": "12 AZN",
        "link": "https://t.me/taha_onlayn_satis/991"
    }
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🌦️ Hava", "📚 Kitablar")
    bot.send_message(message.chat.id, "Xoş gəlmisiniz! Aşağıdakı düymələrdən istifadə edə bilərsiniz:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text is not None)
def handle_message(message):
    text = message.text.lower()
    time.sleep(1)

    if text in ["🌦️ hava", "hava"]:
        bot.reply_to(message, get_weather("Bakı"))

    elif text in ["📚 kitablar", "kitablar"]:
        msg = ""
        for book in BOOK_CATALOG:
            msg += f"📘 <b>{book['title']}</b>\n"
            msg += f"✍️ Müəllif: {book['author']}\n"
            msg += f"📄 {book['description']}\n"
            msg += f"💰 Qiymət: {book['price']}\n"
            msg += f"🔗 <a href='{book['link']}'>Kitaba bax</a>\n\n"
        bot.send_message(message.chat.id, msg, parse_mode="HTML", disable_web_page_preview=False)

    elif "hava" in text:
        city = text.replace("hava", "").strip()
        msg = get_weather(city) if city else "Zəhmət olmasa şəhər adını daxil edin."
        bot.reply_to(message, msg)

    elif "kitab" in text:
        query = text.replace("kitab", "").strip()
        msg = search_books(query) if query else "Zəhmət olmasa kitab adı yazın."
        bot.reply_to(message, msg)

    elif any(word in text for word in ["salam", "salamm", "salam əleykum", "salam aleykum"]):
        bot.reply_to(message, "Əleykum Salam!")

    elif "necəsən" in text:
        bot.reply_to(message, "Mən yaxşıyam! Sən necəsən?")

    elif "çox sağ ol" in text or "çox sağol" in text:
        bot.reply_to(message, "Dəyməz!")

    elif any(word in text for word in ["qiymət", "neçəyə"]):
        bot.reply_to(message, "Qiymətlər kitabdan asılı olaraq dəyişir.")

    elif any(word in text for word in ["əlaqə", "nömrə"]):
        bot.reply_to(message, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")

    elif any(word in text for word in ["çatdır", "çatdırılma"]):
        bot.reply_to(message, "Çatdırılma Bakıda 1 günə, bölgələrə 2-3 günə çatır.")

    else:
        bot.reply_to(message, "Zəhmət olmasa telefon nömrənizi və ünvanınızı da əlavə edin.")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=az"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{city.capitalize()} şəhərində hava: {data['weather'][0]['description']}, {data['main']['temp']}°C."
    return "Şəhər tapılmadı və ya hava məlumatı mövcud deyil."

def search_books(query):
    query = query.lower()
    results = []
    for book in BOOK_CATALOG:
        if query in book["title"].lower():
            results.append(
                f"📘 <b>{book['title']}</b>\n"
                f"✍️ Müəllif: {book['author']}\n"
                f"📄 {book['description']}\n"
                f"💰 Qiymət: {book['price']}\n"
                f"🔗 <a href='{book['link']}'>Kitaba bax</a>"
            )
    return "\n\n".join(results) if results else "Axtardığınız kitaba uyğun nəticə tapılmadı."

@app.route('/')
def index():
    return "Bot işləyir!"

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return 'ok', 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://tahastorebot.onrender.com/' + TOKEN)
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
