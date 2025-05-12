import telebot
import requests
import json
import os
from flask import Flask, request
import base64
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Spotify funksiyaları
def get_spotify_token():
    auth_str = f"{SPOTIFY_CLIENT_ID a38a69ca13934b59b7f7728f41eaa7f4}:{SPOTIFY_CLIENT_SECRET 9591ded7346c4a0aad90af7d084cd295}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
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

# Əsas mesaj cavablayıcı
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if text == "/start":
        bot.send_message(message.chat.id, "Salam! Axtarış etmək istədiyiniz mahnının adını yazın. Məs: Pərviz Hüseyni")

    elif any(name in text for name in ["pərviz hüseyni", "baqir mənsuri", "islami mahnılar", "mərsiyə"]):
        bot.send_chat_action(message.chat.id, "typing")
        result = search_spotify(text)
        bot.send_message(message.chat.id, result, parse_mode="HTML", disable_web_page_preview=False)

    else:
        bot.send_message(message.chat.id, "Axtardığınız ifadə üzrə nəticə tapılmadı. Zəhmət olmasa dəqiq ifadə daxil edin.")

# Webhook və Flask
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "", 200

@app.route("/")
def index():
    return "Bot işə düşdü!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://tahastorebot.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
