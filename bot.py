import telebot
from flask import Flask, request
import os
import threading

TOKEN = "7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI"
bot = telebot.TeleBot(TOKEN)

# ✅ Mesaj cavablandırma funksiyası
@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
    print(f"Gələn mesaj: {message.text}")

    text = message.text.lower()

    # Açar sözlərə uyğun cavablar
    if any(word in text for word in ["salam", "salammm", "salamm"]):
        bot.reply_to(message, "Salam! Necə kömək edə bilərəm?")
    elif "necəsən" in text:
        bot.reply_to(message, "Mən yaxşıyam, sağ ol! Sən necəsən?")
    elif "kitab" in text:
        bot.reply_to(message, "Hansı janrda kitab axtarırsınız?")
    elif any(word in text for word in ["qiymət", "neçəyə"]):
        bot.reply_to(message, "Qiymətlər kitabdan asılı olaraq dəyişir.")
    elif any(word in text for word in ["əlaqə", "nömrə"]):
        bot.reply_to(message, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    elif any(word in text for word in ["çatdır", "çatdırılma"]):
        bot.reply_to(message, "Çatdırılma Bakıda 1 günə, bölgələrə 2-3 günə çatır.")
    else:
        bot.reply_to(message, "Zəhmət olmasa telefon nömrənizi və ünvanınızı da əlavə edin.")

# Flask hissəsi
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot işləyir!"

def run_bot():
    print("Bot başlamalıdır...")
    bot.remove_webhook()
    bot.set_webhook(url='https://tahastorebot.onrender.com/' + TOKEN)
    print("Webhook quruldu.")

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return 'ok', 200

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
