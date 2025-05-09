import telebot
from flask import Flask, request
import os
import requests

TOKEN = "7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Weather və kitab axtarışı üçün açarlar
WEATHER_API_KEY = "8db207e04b11bb5027922faf1eeee944"
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# Mesajlara cavab
@bot.message_handler(func=lambda message: message.text is not None)
def handle_message(message):
    text = message.text.lower()

    if "hava" in text:
        city = text.replace("hava", "").strip()
        msg = get_weather(city) if city else "Zəhmət olmasa şəhər adını daxil edin."
        bot.reply_to(message, msg)

    elif "kitab" in text:
        query = text.replace("kitab", "").strip()
        msg = search_books(query) if query else "Zəhmət olmasa kitab adı yazın."
        bot.reply_to(message, msg)

    elif any(word in text for word in ["salam", "salamm"]):
        bot.reply_to(message, "Salam! Necə kömək edə bilərəm?")
    elif "necəsən" in text:
        bot.reply_to(message, "Mən yaxşıyam! Sən necəsən?")
    elif any(word in text for word in ["qiymət", "neçəyə"]):
        bot.reply_to(message, "Qiymətlər kitabdan asılı olaraq dəyişir.")
    elif any(word in text for word in ["əlaqə", "nömrə"]):
        bot.reply_to(message, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    elif any(word in text for word in ["çatdır", "çatdırılma"]):
        bot.reply_to(message, "Çatdırılma Bakıda 1 günə, bölgələrə 2-3 günə çatır.")
    else:
        bot.reply_to(message, "Zəhmət olmasa telefon nömrənizi və ünvanınızı da əlavə edin.")

# Hava məlumatı
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{city.capitalize()} şəhərində hava: {data['weather'][0]['description']}, {data['main']['temp']}°C."
    return "Şəhər tapılmadı və ya hava məlumatı mövcud deyil."

# Kitab axtarışı
def search_books(query):
    url = f"{GOOGLE_BOOKS_API_URL}?q={query}"
    response = requests.get(url)
    if "items" in response.json():
        results = []
        for book in response.json()["items"][:3]:
            title = book["volumeInfo"].get("title", "Başlıq tapılmadı")
            authors = ", ".join(book["volumeInfo"].get("authors", ["Müəllif yoxdur"]))
            results.append(f"📘 {title}\n✍️ {authors}\n")
        return "\n".join(results)
    return "Axtarışa uyğun kitab tapılmadı."

# Flask
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
