import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from deep_translator import GoogleTranslator

# @BotFather bergan tokenni shu yerga yozing:
TOKEN = "7932048703:AAELpPeRoPJjYqMpTcUvI_OcOLl0_kF5fSg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start buyrug'i uchun buyruqlovchi
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Salom! Men tarjimon botman.\n\n"
        "Menga har qanday matn yuboring:\n"
        "• Lotin yoki Kirill matn yuborsangiz — **Ingliz tiliga** tarjima qilaman.\n"
        "• Boshqa tillardagi matnlarni — **O'zbek tiliga** tarjima qilaman."
    )

# Matnlarni tarjima qilish handler'i
@dp.message()
async def translate_handler(message: types.Message):
    user_text = message.text
    
    try:
        # Avval matn tilini aniqlash uchun translator
        translator = GoogleTranslator(source='auto', target='uz')
        
        # Avto-aniqlangan tilni tekshiramiz
        detected_lang = translator.detect(user_text)
        
        # Agar o'zbekcha bo'lsa -> Ingliz tiliga, boshqa dil bo'lsa -> O'zbek tiliga
        if detected_lang in ['uz', 'uzbek']:
            target_lang = 'en'
        else:
            target_lang = 'uz'
            
        translated = GoogleTranslator(source='auto', target=target_lang).translate(user_text)
        
        await message.reply(f"🔠 Tarjima ({target_lang.upper()}):\n\n{translated}")
    except Exception as e:
        # Sodda tarjima varianti (xatolik beringanda)
        try:
            translated = GoogleTranslator(source='auto', target='uz').translate(user_text)
            await message.reply(f"🔠 Tarjima:\n\n{translated}")
        except Exception as err:
            await message.reply("Xatolik yuz berdi. Matnni qayta yuborib ko'ring.")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
