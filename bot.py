import telebot
import requests
import json
import os
from flask import Flask, request
import base64
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
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
    elif "necəsən?", in text or "yaxşısan?", in text or "necəsən":
        bot.send_message(chat_id, "Şükür mən yaxşıyam! Sən necəsən?")
    elif "çox sağ ol", in text or "çox sağol", in text or "təşəkkür", in text or "yaxşıyam", in text or "Şükür Allaha salamatlıqdı":
        bot.send_message(chat_id, "Dəyməz, həmişə yaxşı ol! 😊", "həmişə salamatlıq olsun təki")
    elif any(word in text for word in ["qiymət", "neçəyə", "neçəyədır", "neçəyidir", "neçədir"]):
        bot.send_message(chat_id, "Qiymətlər kitabdan asılı olaraq dəyişir. Hansı kitabla maraqlanırsınız?")
    elif any(word in text for word in ["əlaqə", "nömrə"]):
        bot.send_message(chat_id, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    elif any(word in text for word in ["çatdır", "çatdırılma"]):
        bot.send_message(chat_id, "Çatdırılma Bakıda 1 günə, bölgələrə 2-3 günə çatır.")
    elif "səni kim yaradıb" in text:
        bot.send_message(chat_id, "Məni Kamran qardaşım yaradıb! 🤖❤️")
bot.reply_to(...)
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

   elif text == "mp3"
    bot.send_message(chat_id, "Zəhmət olmasa dinləmək istədiyiniz mərsiyə və ya ifaçı adını yazın.")

elif any(keyword in text for keyword in [
    "abasəlt", "əba-əbdillah", "aldı hüseyn", "anam zəhra", "ləbeyk", "ya əli", "ya huseyn",
    "ruqəyyə", "zəhra", "sahibi zaman", "əli mövla", "əli əkbər", "əlinin yari", "zeynəb", "lay-lay"
]):

    drive_links = {
        if 'abasəlt ebrahimi - abufazil' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1bCAe_7IjAbcZVGNNFvG01MXYZ')
    elif 'abasəlt ebrahimi - aldı hüseyn qan ilə bir dəstəmaz' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1cDEf_8KjBcYZWGNNFvG02NABC')
    elif 'abasəlt ebrahimi - hüseyn əba-əbdillah' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1dEFg_9LkCdZXWHNNFvG03NDEF')
    elif 'abasəlt ebrahimi - ləbbeyk ya əba-əbdillah' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1eFGh_0MlDeAYXINNFvG04NGHI')
    elif 'adel najafi - hz. əbəlfəzl' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1fGHi_1NmEfBZYOONFvG05NJJK')
    elif 'hacı islam mirzai - anam zəhra' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1gHIj_2OnFgCZZPPNFvG06NKLM')
    elif 'baqir mənsuri - ruqəyyə nazlı surətin' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1hIJk_3PoGhDAAQQNFvG07NLMN')
    elif 'ceyhun müəzzin - əli mövla' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1iJKl_4QpHiEBBRRNFvG08NMOP')
    elif 'əhlibeyt qrupu - əli əkbər' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1jKLm_5RqIjFCCSSNFvG09NPQR')
    elif 'əhlibeyt qrupu - sahibi zaman gəldi' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1kLMn_6SrJkGDDTTNFvG10NQRS')
    elif 'əhlibeyt qrupu - ya əli' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1lMNo_7TsKlHEEUUNFvG11NRTS')
    elif 'əkbər babazadə - əli lay-lay gülüm lay-lay' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1mNOp_8UtLmIFFVVNFvG12NSUV')
    elif 'mehdi rəsuli - əlini ağlatma' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1nOPq_9VuMnJGGWWNFvG13NTVW')
    elif 'baqir mənsuri - əlinin yari zəhra' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1oPQr_0WvNoKHHXXNFvG14NUWX')
    elif 'baqir mənsuri - ağlaram zəhra' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1pQRs_1XwOpLIYYYNFvG15NVXY')
    elif 'baqir mənsuri - ağlama xudahafiz' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1qRSt_2YxPqMJZZZNFvG16NWYZ')
    elif 'hacı kamran - yaralı zəhra' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1rSTu_3ZyQrNKAAANFvG17NXZA')
    elif 'hacı kamran - ya hüseyn' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1sTUV_4AzRsOLBBBNFvG18NYAB')
    elif 'hacı zahir - gözün aç zəhra' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1tUVW_5BaStPMCCCCNFvG19NZBC')
    elif 'hadi kazemi - babəl hüseyn' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1uVWX_6CbTuQNDDDNFvG20NACD')
    elif 'hadi kazemi - həbibi ya hüseyn' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1vWXY_7DcUvREDDDEFvG21NBDC')
    elif 'hadi kazemi - məzlum əli' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1wXYZ_8EdVwSFEFFNFvG22NCEC')
    elif 'hadi kazemi - million army' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1xYZA_9FeWxTGFGGNFvG23NDFC')
    elif 'həsən neməti - salam qarə pərçəmə' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1yZAB_0GfXyUHGHHNFvG24NEGC')
    elif 'əkbər babazadə - qara köynək geyərəm' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1zABC_1HgYzVIIIIIFvG25NFHC')
    elif 'səlim müəzzinzadə - zeynəb zeynəb' in text:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio='https://drive.google.com/uc?export=download&id=1aBCD_2IhAzWJJJJJFvG26NGIC')
    else:
        update.message.reply_text('Bağışlayın, bu mahnını tapa bilmədim.')
# burda sən istədikcə əlavə edə bilərsən
    }

    found = False
    for keyword, link in drive_links.items():
        if keyword in text:
            bot.send_message(chat_id, f"Dinlə: {link}")
            found = True
            break

    if not found:
        bot.send_message(chat_id, "Mahnı tapılmadı. Zəhmət olmasa daha dəqiq yazın.")

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

