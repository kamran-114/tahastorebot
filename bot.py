import telebot
import requests
import json
import os
from flask import Flask, request
import base64
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Kitab məlumatları
books = {
    "Dini Kitablar": {
        "Hədislər": [
            {
                "ad": "Qütbü Sitte",
                "müəllif": "Buxari",
                "haqqinda": "Səhih hədislər toplusudur.",
                "qiymet": "12 AZN"
            },
            {
                "ad": "Nəhcül Bəlağə",
                "müəllif": "İmam Əli",
                "haqqinda": "İmam Əlinin xütbələri və məktubları.",
                "qiymet": "15 AZN"
            }
        ]
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Kitablar", "MP3", "Hava", "Əlaqə")
    bot.send_message(message.chat.id, "Salam! Nə ilə maraqlanırsan?", reply_markup=markup)

def get_spotify_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {b64_auth_str}"},
        data={"grant_type": "client_credentials"}
    )
    return response.json().get("access_token") if response.status_code == 200 else None

def search_spotify(query):
    token = get_spotify_token()
    if not token:
        return "Spotify ilə əlaqə qurulmadı."

    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 3}
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if response.status_code != 200:
        return "Mahnı tapılmadı."

    tracks = response.json().get("tracks", {}).get("items", [])
    if not tracks:
        return "Nəticə tapılmadı."

    result_message = ""
    for track in tracks:
        name = track["name"]
        artists = ", ".join([artist["name"] for artist in track["artists"]])
        url = track["external_urls"]["spotify"]
        result_message += f"🎧 <b>{name}</b> - {artists}\n🔗 <a href='{url}'>Spotify'da dinlə</a>\n\n"

    return result_message.strip()

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=az"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "Hava məlumatı tapılmadı."

    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    name = data["name"]
    
    return f"{name} şəhərində hava: {desc}, temperatur: {temp}°C"

def handle_dialogs(text, chat_id):
    if any(word in text for word in ["salam", "salamm", "salam əleykum", "salam aleykum"]):
        bot.send_message(chat_id, "Əleykum Salam!")
    elif "necəsən" in text:
        bot.send_message(chat_id, "Mən yaxşıyam! Sən necəsən?")
    elif "çox sağ ol" in text or "çox sağol" in text or "təşəkkür" in text:
        bot.send_message(chat_id, "Dəyməz, həmişə yaxşı ol! 😊")
    elif any(word in text for word in ["qiymət", "neçəyə", "neçəyədır", "neçəyidir", "neçədir"]):
        bot.send_message(chat_id, "Qiymətlər kitabdan asılı olaraq dəyişir. Hansı kitabla maraqlanırsınız?")
    elif any(word in text for word in ["əlaqə", "nömrə"]):
        bot.send_message(chat_id, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    elif any(word in text for word in ["çatdır", "çatdırılma"]):
        bot.send_message(chat_id, "Çatdırılma Bakıda 1 günə, bölgələrə 2-3 günə çatır.")
    elif "səni kim yaradıb" in text:
        bot.send_message(chat_id, "Məni Kamran qardaşım yaradıb! 🤖❤️")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    chat_id = message.chat.id

    if text == "kitablar":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Hədislər", "🔙 Geri")
        bot.send_message(chat_id, "Zəhmət olmasa bölmə seçin:", reply_markup=markup)

    elif text == "hədislər":
        for kitab in books["Dini Kitablar"]["Hədislər"]:
            msg = f"📘 <b>{kitab['ad']}</b>\n✍️ Müəllif: {kitab['müəllif']}\nℹ️ {kitab['haqqinda']}\n💰 Qiymət: {kitab['qiymet']}"
            bot.send_message(chat_id, msg, parse_mode="HTML")

    elif text == "mp3":
        bot.send_message(chat_id, "Zəhmət olmasa axtaracağınız mahnı adını yazın.")

    elif text == "hava":
        bot.send_message(chat_id, "Zəhmət olmasa şəhər adını yazın.")

    elif text == "əlaqə":
        bot.send_message(chat_id, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")

    elif text == "🔙 geri":
        send_welcome(message)

    elif text in ["sami yusuf", "pərviz hüseyni", "baqir mənsuri", "mərsiyələr"]:
        result = search_spotify(text)
        bot.send_message(chat_id, result, parse_mode="HTML", disable_web_page_preview=True)

    elif text.isalpha() and len(text) > 2:
        weather_result = get_weather(text)
        bot.send_message(chat_id, weather_result)

    else:
        handle_dialogs(text, chat_id)

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
