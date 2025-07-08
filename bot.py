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
        mp3_links = {
    "abasəlt ebrahimi - abufazil(ə)": "https://drive.google.com/uc?export=download&id=1LUxfbVpi_aEV-V1De2scwCUtJ1jP1o_Y",
    "abasəlt ebrahimi - aldı hüseyn qan ilə bir dəstəmaz": "https://drive.google.com/uc?export=download&id=1cDEf_8KjBcYZWGNNFvG02NABC",
    "abasəlt ebrahimi - hüseyn əba-əbdillah": "https://drive.google.com/uc?export=download&id=1dEFg_9LkCdZXWHNNFvG03NDEF",
    "abasəlt ebrahimi - ləbbeyk ya əba-əbdillah": "https://drive.google.com/uc?export=download&id=1eFGh_0MlDeAYXINNFvG04NGHI",
    "adel najafi - hz. əbəlfəzl": "https://drive.google.com/uc?export=download&id=1fGHi_1NmEfBZYOONFvG05NJJK",
    "hacı islam mirzai - anam zəhra": "https://drive.google.com/uc?export=download&id=1gHIj_2OnFgCZZPPNFvG06NKLM",
    "baqir mənsuri - ruqəyyə nazlı surətin": "https://drive.google.com/uc?export=download&id=1hIJk_3PoGhDAAQQNFvG07NLMN",
    "ceyhun müəzzin - əli mövla": "https://drive.google.com/uc?export=download&id=1iJKl_4QpHiEBBRRNFvG08NMOP",
    "əhlibeyt qrupu - əli əkbər": "https://drive.google.com/uc?export=download&id=1jKLm_5RqIjFCCSSNFvG09NPQR",
    "əhlibeyt qrupu - sahibi zaman gəldi": "https://drive.google.com/uc?export=download&id=1kLMn_6SrJkGDDTTNFvG10NQRS",
    "əhlibeyt qrupu - ya əli": "https://drive.google.com/uc?export=download&id=1lMNo_7TsKlHEEUUNFvG11NRTS",
    "əkbər babazadə - əli lay-lay gülüm lay-lay": "https://drive.google.com/uc?export=download&id=1mNOp_8UtLmIFFVVNFvG12NSUV",
    "mehdi rəsuli - əlini ağlatma": "https://drive.google.com/uc?export=download&id=1nOPq_9VuMnJGGWWNFvG13NTVW",
    "baqir mənsuri - əlinin yari zəhra": "https://drive.google.com/uc?export=download&id=1oPQr_0WvNoKHHXXNFvG14NUWX",
    "baqir mənsuri - ağlaram zəhra": "https://drive.google.com/uc?export=download&id=1pQRs_1XwOpLIYYYNFvG15NVXY",
    "baqir mənsuri - ağlama xudahafiz": "https://drive.google.com/uc?export=download&id=1qRSt_2YxPqMJZZZNFvG16NWYZ",
    "hacı kamran - yaralı zəhra": "https://drive.google.com/uc?export=download&id=1rSTu_3ZyQrNKAAANFvG17NXZA",
    "hacı kamran - ya hüseyn": "https://drive.google.com/uc?export=download&id=1sTUV_4AzRsOLBBBNFvG18NYAB",
    "hacı zahir - gözün aç zəhra": "https://drive.google.com/uc?export=download&id=1tUVW_5BaStPMCCCCNFvG19NZBC",
    "hadi kazemi - babəl hüseyn": "https://drive.google.com/uc?export=download&id=1uVWX_6CbTuQNDDDNFvG20NACD",
    "hadi kazemi - həbibi ya hüseyn": "https://drive.google.com/uc?export=download&id=1vWXY_7DcUvREDDDEFvG21NBDC",
    "hadi kazemi - məzlum əli": "https://drive.google.com/uc?export=download&id=1wXYZ_8EdVwSFEFFNFvG22NCEC",
    "hadi kazemi - million army": "https://drive.google.com/uc?export=download&id=1xYZA_9FeWxTGFGGNFvG23NDFC",
    "həsən neməti - salam qarə pərçəmə": "https://drive.google.com/uc?export=download&id=1yZAB_0GfXyUHGHHNFvG24NEGC",
    "əkbər babazadə - qara köynək geyərəm": "https://drive.google.com/uc?export=download&id=1zABC_1HgYzVIIIIIFvG25NFHC",
    "səlim müəzzinzadə - zeynəb zeynəb": "https://drive.google.com/uc?export=download&id=1aBCD_2IhAzWJJJJJFvG26NGIC"
}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    chat_id = message.chat.id

    # mp3 yoxlaması
    for key in mp3_links:
        if key in text:
            bot.send_audio(chat_id, mp3_links[key])
            return

    # burda digər funksiyalar davam edir
    # məsələn kitablar, hava, dialoglar və s.


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
