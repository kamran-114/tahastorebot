import telebot
from flask import Flask, request
import os
import requests
import time
from telebot import types
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

TOKEN = "7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

WEATHER_API_KEY = "8db207e04b11bb5027922faf1eeee944"

SPOTIFY_CLIENT_ID = "b804430eb5f8457ea58200c0c6e857be"
SPOTIFY_CLIENT_SECRET = "424fce5b09194c7eb6811b70039f70f1"

# Spotify API ayarları
spotify_auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(auth_manager=spotify_auth_manager)

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
    markup.row("🌦️ Hava", "📚 Kitablar", "🎧 Spotify")
    bot.send_message(message.chat.id, "Xoş gəlmisiniz! Aşağıdakı düymələrdən istifadə edə bilərsiniz:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text is not None)
def handle_message(message):
    text = message.text.lower().strip()
    time.sleep(1)

    if text in ["hava", "🌦️ hava"]:
        bot.reply_to(message, get_weather("Bakı"))

    elif text in ["kitablar", "📚 kitablar"]:
        msg = ""
        for book in BOOK_CATALOG:
            msg += f"📘 [{book['title']}]({book['link']})\n✍️ Müəllif: {book['author']}\n📄 {book['description']}\n💰 Qiymət: {book['price']}\n\n"
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")

    elif text in ["spotify", "🎧 spotify"]:
        bot.reply_to(message, "Spotify-da axtarmaq istədiyiniz mahnının və ya ifaçının adını yazın (məsələn: *Baqir Mənsuri*).")

    elif "hava" in text:
        city = text.replace("hava", "").strip()
        msg = get_weather(city) if city else "Zəhmət olmasa şəhər adını daxil edin."
        bot.reply_to(message, msg)

    elif "kitab" in text:
        query = text.replace("kitab", "").strip()
        msg = search_books(query) if query else "Zəhmət olmasa kitab adı yazın."
        bot.reply_to(message, msg)

    elif "spotify" in text:
        query = text.replace("spotify", "").strip()
        msg = search_spotify(query) if query else "Zəhmət olmasa axtarmaq istədiyiniz mahnı və ya ifaçını yazın."
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
            results.append(f"📘 [{book['title']}]({book['link']})\n✍️ Müəllif: {book['author']}\n📄 {book['description']}\n💰 Qiymət: {book['price']}\n")
    return "\n\n".join(results) if results else "Axtardığınız kitaba uyğun nəticə tapılmadı."

def search_spotify(query):
    try:
        results = spotify.search(q=query, limit=3, type='track')
        if results['tracks']['items']:
            msg = "🎵 Spotify nəticələri:\n\n"
            for track in results['tracks']['items']:
                name = track['name']
                artist = track['artists'][0]['name']
                url = track['external_urls']['spotify']
                msg += f"🎧 {name} - {artist}\n🔗 [Dinlə]({url})\n\n"
            return msg
        else:
            return "Nəticə tapılmadı."
    except Exception as e:
        return "Spotify məlumatına çatmaq mümkün olmadı."

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
