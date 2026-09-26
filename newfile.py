import telebot
from deep_translator import GoogleTranslator

TOKEN = "7932048703:AAELpPeRoPJjYqMpTcUvl_OcOLI0_kF5fSg"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "Salom! Men tarjimon botman.\n\n"
        "Menga har qanday matn yuboring, men uni O'zbek tiliga tarjima qilib beraman."
    )
    bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        translated = GoogleTranslator(source='auto', target='uz').translate(message.text)
        bot.reply_to(message, f"🔠 Tarjimasi:\n\n{translated}")
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()
