import telebot
from flask import Flask, request
import os
import requests
import threading

TOKEN = "7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI"
bot = telebot.TeleBot(TOKEN)

# OpenWeatherMap API açarınızı burada yerləşdirin
WEATHER_API_KEY = "8db207e04b11bb5027922faf1eeee944"
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# ✅ Mesaj cavablandırma funksiyası
@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
    print(f"Gələn mesaj: {message.text}")

    text = message.text.lower()

    # Hava məlumatları üçün axtarış
    if "hava" in text:
        city = text.replace("hava", "").strip()
        if city:
            weather = get_weather(city)
            bot.reply_to(message, weather)
        else:
            bot.reply_to(message, "Zəhmət olmasa şəhər adını daxil edin.")

    # Kitab axtarışı üçün axtarış
    elif "kitab" in text:
        query = text.replace("kitab", "").strip()
        if query:
            books = search_books(query)
            bot.reply_to(message, books)
        else:
            bot.reply_to(message, "Zəhmət olmasa axtarmaq istədiyiniz kitabın adını daxil edin.")

    # Əlavə cavablar
    elif any(word in text for word in ["salam", "salammm", "salamm"]):
        bot.reply_to(message, "Salam! Necə kömək edə bilərəm?")
    elif "necəsən" in text:
        bot.reply_to(message, "Mən yaxşıyam, sağ ol! Sən necəsən?")
    elif any(word in text for word in ["qiymət", "neçəyə"]):
        bot.reply_to(message, "Qiymətlər kitabdan asılı olaraq dəyişir.")
    elif any(word in text for word in ["əlaqə", "nömrə"]):
        bot.reply_to(message, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    elif any(word in text for word in ["çatdır", "çatdırılma"]):
        bot.reply_to(message, "Çatdırılma Bakıda 1 günə, bölgələrə 2-3 günə çatır.")
    else:
        bot.reply_to(message, "Zəhmət olmasa telefon nömrənizi və ünvanınızı da əlavə edin.")

# Hava məlumatı alırıq (OpenWeatherMap API)
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        weather_report = f"{city.capitalize()} şəhərində hava: {description}. Temperatur: {temperature}°C."
        return weather_report
    else:
        return "Şəhər tapılmadı və ya hava məlumatları əldə edilə bilmədi."

# Google Books API istifadə edərək kitab axtarışı
def search_books(query):
    url = f"{GOOGLE_BOOKS_API_URL}?q={query}"
    response = requests.get(url)
    data = response.json()

    if "items" in data:
        books = data["items"]
        results = []

        for book in books[:5]:  # İlk 5 kitabı göstəririk
            title = book["volumeInfo"].get("title", "Başlıq tapılmadı")
            authors = ", ".join(book["volumeInfo"].get("authors", ["Müəllif tapılmadı"]))
            description = book["volumeInfo"].get("description", "Təsvir tapılmadı")
            results.append(f"**{title}**\nMüəllif: {authors}\nTəsvir: {description}\n\n")

        return "\n".join(results)
    else:
        return "Axtarışınıza uyğun heç bir nəticə tapılmadı."

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

