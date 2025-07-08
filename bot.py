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

def handle_dialogs(text, chat_id):
    if any(word in text for word in ["salam", "salamm", "salam əleykum", "salam aleykum"]):
        bot.send_message(chat_id, "Əleykum Salam!")
    elif "necəsən" in text:
        bot.send_message(chat_id, "Şükür mən yaxşıyam! Sən necəsən?")
    elif (
        "çox sağ ol" in text
        or "çox sağol" in text
        or "təşəkkür" in text
        or "yaxşıyam" in text
        or "şükür allaha salamatlıqdı" in text
    ):
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

    elif any(keyword in text for keyword in [
        "əbufazel", "abufazil", "abasəlt", "əba-əbdillah", "aldı hüseyn", "anam zəhra",
        "ləbeyk", "ya əli", "ya huseyn", "ruqəyyə", "zəhra", "sahibi zaman",
        "əli mövla", "əli əkbər", "əlinin yari", "zeynəb", "lay-lay"
    ]):
        drive_links = {
            "əbufazel": "https://drive.google.com/uc?export=download&id=1LUxfbVpi_aEV-V1De2scwCUtJ1jP1o_Y",
            "abufazil": "https://drive.google.com/uc?export=download&id=1LUxfbVpi_aEV-V1De2scwCUtJ1jP1o_Y"
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
            # Digər mp3-ləri də bura əlavə edə bilərsən
        }
        found = False
        for keyword, link in drive_links.items():
            if keyword in text:
                bot.send_audio(chat_id, audio=link)
                found = True
                break
        if not found:
            bot.send_message(chat_id, "Mahnı tapılmadı. Zəhmət olmasa daha dəqiq yazın.")

    elif text in ["sami yusuf", "pərviz hüseyni", "baqir mənsuri", "mərsiyələr"]:
        result = search_spotify(text)
        bot.send_message(chat_id, result, parse_mode="HTML", disable_web_page_preview=True)

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
