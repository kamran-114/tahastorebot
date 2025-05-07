import telebot

bot = telebot.TeleBot("7636424888:AAH58LLAzt3ycad8Q7UMTVMnAW9IPeLTUOI")

# Komandalar üçün
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "Salam! Mənə kitablarla bağlı suallar verə bilərsən.")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Mən sizə kitablar haqqında kömək edə bilərəm. Əgər almaq istədiyiniz kitabı bilmirsinizsə, mənə deyə bilərsiniz.")

@bot.message_handler(commands=['info'])
def info_command(message):
    bot.reply_to(message, "Bu bot kitab satışını asanlaşdırmaq məqsədilə yaradılıb. Məlumat üçün yazın!")

@bot.message_handler(commands=['hello'])
def hello_command(message):
    bot.reply_to(message, "Salam! Necəsən? Kitab haqqında nə sualınız var?")

# Sıradan mesajlar üçün (komanda olmayanlar)
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_message(message):
    text = message.text.lower()

    if "kitab" in text:
        bot.reply_to(message, "Hansı janrda kitab axtarırsınız?")
    elif "qiymət" in text:
        bot.reply_to(message, "Qiymətlər kitabdan asılı olaraq dəyişir.")
    elif "əlaqə" in text or "nömrə" in text:
        bot.reply_to(message, "Bizim əlaqə nömrəmiz: +994 XX XXX XX XX")
    else:
        bot.reply_to(message, "Zəhmət olmasa telefon nömrənizi və ünvanınızı da əlavə edin.")

# polling bir dəfə olmalıdır
bot.polling()
