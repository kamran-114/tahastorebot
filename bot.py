import telebot
import requests
import json
import os
from flask import Flask, request
import base64
from dotenv import load_dotenv

# .env faylını yüklə
load_dotenv()

# Ətraf mühit dəyişənlərini götür
BOT_TOKEN = os.getenv("BOT_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Telebot obyektini yarat
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Spotify funksiyaları
def get_spotify_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {b64_auth_str}"},
        data={"grant_type": "client_credentials"}
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None

def search_spotify(query):
    token = get_spotify_token()
    if not token:
        return "Spotify ilə əlaqə qurulmadı."

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": "track",
        "limit": 5
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if response.status_code != 200:
        return "Mahnı tapılmadı."

    data = response.json()
    tracks = data.get("tracks", {}).get("items", [])
    if not tracks:
        return "Nəticə tapılmadı."

    msg = "🎵 Tapılan mahnılar:\n\n"
    for track in tracks:
        name = track["name"]
        artists = ", ".join([artist["name"] for artist in track["artists"]])
        url = track["external_urls"]["spotify"]
        msg += f"🎧 <b>{name}</b> - {artists}\n🔗 <a href='{url}'>Spotify'da dinlə</a>\n\n"

    return msg

# Kitab məlumatları nümunəsi
books = {
    "Dini Kitablar": {
        "Hədislər": [
            {
                "ad": "Kafi (1-ci cild)",
                "müəllif": "Şeyx Kuleyni",
                "haqqinda": "Əhli-beyt hədislərini əhatə edən mötəbər mənbələrdən biridir.",
                "qiymet": "12 AZN"
            },
            {
                "ad": "Səfinətül-Bihar",
                "müəllif": "Şeyx Abbas Qummi",
                "haqqinda": "Biharül-Ənvar əsərinin xülasəsidir.",
                "qiymet": "10 AZN"
            }
        ]
    }
}

# Əsas menyu
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Dini Kitablar")
    bot.send_message(message.chat.id, "Salam! Nə ilə maraqlanırsan?", reply_markup=markup)

# İstifadəçi mesajını idarə et
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if text == "dini kitablar":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Hədislər", "🔙 Geri")
        bot.send_message(message.chat.id, "Zəhmət olmasa bölmə seçin:", reply_markup=markup)

    elif text == "hədislər":
        for kitab in books["Dini Kitablar"]["Hədislər"]:
            msg = f"📘 <b>{kitab['ad']}</b>\n✍️ Müəllif: {kitab['müəllif']}\nℹ️ {kitab['haqqinda']}\n💰 Qiymət: {kitab['qiymet']}"
            bot.send_message(message.chat.id, msg, parse_mode="HTML")

    elif text == "🔙 geri":
        send_welcome(message)

    elif any(name in text for name in ["pərviz hüseyni", "baqir mənsuri", "islami mahnılar", "mərsiyə"]):
        bot.send_chat_action(message.chat.id, "typing")
        result = search_spotify(text)
        bot.send_message(message.chat.id, result, parse_mode="HTML", disable_web_page_preview=False)

    else:
        bot.send_message(message.chat.id, "Axtardığınız ifadə üzrə nəticə tapılmadı və ya seçim mövcud deyil.")

# Webhook və Flask
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "", 200

@app.route("/")
def index():
    return "Bot işə düşdü!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://tahastorebot.onrender.com/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
