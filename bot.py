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
    elif any(word in text for word in ["çox sağ ol", "çox sağol", "təşəkkür", "yaxşıyam", "şükür Allaha salamatlıqdı"]):
        bot.send_message(chat_id, "Dəyməz, həmişə yaxşı ol! 😊")
    elif any(word in text for word in ["qiymət", "neçəyə", "neçəyədır", "neçəyidir", "neçədir"]):
        bot.send_message(chat_id, "Qiymətlər kitabdan asılı olaraq dəyişir. Hansı kitabla maraqlanırsınız?")
    elif any(word in text for word in ["əlaqə", "nömrə"]):
        bot.send_message(chat_id, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    elif any(word in text for word in ["çatdır", "çatdırılma"]):
        bot.send_message(chat_id, "Çatdırılma Bakıda 1 günə, bölgələrə 2-3 günə çatır.")
    elif "səni kim yaradıb" in text:
        bot.send_message(chat_id, "Məni Kamran qardaşım yaradıb! 🤖❤️")

# MP3 linkləri
mp3_links = {
    mp3_links = {
    "Abasəlt Ebrahimi - Abufazil(ə)": "https://drive.google.com/uc?export=download&id=1a2b3c4d5e6f7g8h9i0j",
    "Abasəlt Ebrahimi - Aldı Hüseyn(s) qan ilə bir dəstəmaz": "https://drive.google.com/uc?export=download&id=2b3c4d5e6f7g8h9i0j1a",
    "Abasəlt Ebrahimi - Huseyn Əba-Əbdillah(s)": "https://drive.google.com/uc?export=download&id=3c4d5e6f7g8h9i0j1a2b",
    "Abasəlt Ebrahimi - Ləbbeyk ya Əba-Əbdillah(s)": "https://drive.google.com/uc?export=download&id=4d5e6f7g8h9i0j1a2b3c",
    "Adel Najafi - Hz. Əbəlfəzl(ə)": "https://drive.google.com/uc?export=download&id=5e6f7g8h9i0j1a2b3c4d",
    "Hacı İslam Mirzai - Anam Zəhra(s)": "https://drive.google.com/uc?export=download&id=6f7g8h9i0j1a2b3c4d5e",
    "Baqir Mənsuri - Ruqəyyə(s) Nazlı surətin": "https://drive.google.com/uc?export=download&id=7g8h9i0j1a2b3c4d5e6f",
    "Ceyhun Müəzzin - Əli Mövla(s)": "https://drive.google.com/uc?export=download&id=8h9i0j1a2b3c4d5e6f7g",
    "Əhlibeyt qrupu - Əli Əkbər(ə)": "https://drive.google.com/uc?export=download&id=9i0j1a2b3c4d5e6f7g8h",
    "Əhlibeyt qrupu - Sahibi Zaman(s) gəldi": "https://drive.google.com/uc?export=download&id=0j1a2b3c4d5e6f7g8h9i",
    "Əhlibeyt qrupu - Ya Əli(s)": "https://drive.google.com/uc?export=download&id=1k2l3m4n5o6p7q8r9s0t",
    "Əkbər Babazadə - Əli(ə) lay-lay gülüm lay-lay": "https://drive.google.com/uc?export=download&id=2l3m4n5o6p7q8r9s0t1k",
    "Mehdi Rəsuli - Əlini ağlatma": "https://drive.google.com/uc?export=download&id=3m4n5o6p7q8r9s0t1k2l",
    "Baqir Mənsuri(r) - Əlinin yari Zəhra": "https://drive.google.com/uc?export=download&id=4n5o6p7q8r9s0t1k2l3m",
    "Baqir Mənsuri(r) - Ağlaram Zəhra": "https://drive.google.com/uc?export=download&id=5o6p7q8r9s0t1k2l3m4n",
    "Baqir Mənsuri(r) - Ağlama Xudahafiz": "https://drive.google.com/uc?export=download&id=6p7q8r9s0t1k2l3m4n5o",
    "Hacı Kamran(r) - Yaralı Zəhra(s)": "https://drive.google.com/uc?export=download&id=7q8r9s0t1k2l3m4n5o6p",
    "Hacı Kamran(r) - Ya Huseyn(s)": "https://drive.google.com/uc?export=download&id=8r9s0t1k2l3m4n5o6p7q",
    "Hacı Zahir - Gözün aç Zəhra(s)": "https://drive.google.com/uc?export=download&id=9s0t1k2l3m4n5o6p7q8r",
    "Hadi Kazemi - Babəl Hüseyn(s)": "https://drive.google.com/uc?export=download&id=0t1k2l3m4n5o6p7q8r9s",
    "Hadi Kazemi - Həbibi ya Hüseyn(s)": "https://drive.google.com/uc?export=download&id=1u2v3w4x5y6z7a8b9c0d",
    "Hadi Kazemi - Məzlum Əli(s)": "https://drive.google.com/uc?export=download&id=2v3w4x5y6z7a8b9c0d1u",
    "Hadi Kazemi - Million Army": "https://drive.google.com/uc?export=download&id=3w4x5y6z7a8b9c0d1u2v",
    "Həsən Neməti - Salam qarə pərçəmə": "https://drive.google.com/uc?export=download&id=4x5y6z7a8b9c0d1u2v3w",
    "Əkbər Babazadə - Qara köynək geyərəm": "https://drive.google.com/uc?export=download&id=5y6z7a8b9c0d1u2v3w4x",
    "Səlim Müəzzinzadə(r) - Zeynəb Zeynəb": "https://drive.google.com/uc?export=download&id=6z7a8b9c0d1u2v3w4x5y"
}
    # ... digər faylları da əlavə edəcəyik ...
}

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
        bot.send_message(chat_id, "Zəhmət olmasa dinləmək istədiyiniz mərsiyə və ya ifaçı adını yazın.")

    elif text in mp3_links:
        bot.send_audio(chat_id, audio=mp3_links[text])

    elif text == "hava":
        bot.send_message(chat_id, "Zəhmət olmasa şəhər adını yazın.")

    elif text == "əlaqə":
        bot.send_message(chat_id, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")

    elif text == "🔙 geri":
        send_welcome(message)

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
