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
        "title": "Müsəlmanlığın əsasları",
        "author": "Əbu Həmid əl-Qəzzali",
        "description": "İslamın təməl prinsiplərini izah edən klassik əsər.",
        "price": "6 AZN",
        "link": "https://t.me/taha_onlayn_satis/991"
    },
    {
        "title": "Əl-Kafi (Hədislər toplusu)",
        "author": "Kuleyni",
        "description": "Şiə hədislərinin əsas mənbələrindən biri.",
        "price": "10 AZN",
        "link": "https://t.me/taha_onlayn_satis/992"
    },
    {
        "title": "Namazın sirri",
        "author": "Murtəza Mutəhhəri",
        "description": "Namazın mənəvi tərəflərini izah edən dərin əsər.",
        "price": "5 AZN",
        "link": "https://t.me/taha_onlayn_satis/993"
    }
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Hava", "Kitablar")
    bot.send_message(message.chat.id, "Xoş gəlmisiniz! Aşağıdakı düymələrdən istifadə edə bilərsiniz:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text is not None)
def handle_message(message):
    text = message.text.lower()
    time.sleep(1)

    if text == "hava":
        bot.reply_to(message, get_weather("Bakı"))

    elif text == "kitablar":
        markup = types.InlineKeyboardMarkup()
        for i, book in enumerate(BOOK_CATALOG):
            markup.add(types.InlineKeyboardButton(text=book['title'], callback_data=f"book_{i}"))
        bot.send_message(message.chat.id, "📚 Mövcud kitablar:", reply_markup=markup)

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

@bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
def handle_book_callback(call):
    index = int(call.data.split("_")[1])
    book = BOOK_CATALOG[index]
    msg = f"📘 <b>{book['title']}</b>\n" \
          f"✍️ <b>Müəllif:</b> {book['author']}\n" \
          f"📄 <b>Haqqında:</b> {book['description']}\n" \
          f"💰 <b>Qiymət:</b> {book['price']}\n" \
          f"🔗 <a href=\"{book['link']}\">Linkə keçid</a>"
    bot.send_message(call.message.chat.id, msg, parse_mode="HTML")

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
            results.append(f"📘 {book['title']}\n✍️ Müəllif: {book['author']}\n📄 {book['description']}\n💰 Qiymət: {book['price']}\n🔗 Link: {book['link']}")
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
