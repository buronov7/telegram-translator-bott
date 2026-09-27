import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # bir xil natija chiqishi uchun

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Token environment variable orqali olinadi (kodga yozilmaydi!)
BOT_TOKEN = os.environ.get("7932048703:AAELpPeRoPJjYqMpTcUvI_OcOLl0_kF5fSg")

# Tillar: o'zbek, ingliz, rus
LANG_NAMES = {
    "uz": "🇺🇿 Oʻzbekcha",
    "en": "🇬🇧 Inglizcha",
    "ru": "🇷🇺 Ruscha",
}

TARGET_LANGS = ["uz", "en", "ru"]


def detect_language(text: str) -> str:
    """Matn tilini aniqlaydi. langdetect 'uz' ni har doim to'g'ri
    topavermagani uchun oddiy kirill/lotin tekshiruvi bilan kuchaytiramiz."""
    try:
        detected = detect(text)
    except Exception:
        detected = "en"

    # Kirill harflari bo'lsa - ruscha deb hisoblaymiz
    if any("а" <= ch.lower() <= "я" or ch.lower() == "ё" for ch in text):
        return "ru"

    # langdetect ba'zan o'zbekchani boshqa lotin tillar bilan
    # (masalan turkcha, indoneziyacha) adashtiradi
    if detected not in ("en", "ru"):
        return "uz"

    return detected


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Salom! 👋\n\n"
        "Menga oʻzbek, ingliz yoki rus tilida xabar yuboring — "
        "men uni qolgan ikki tilga tarjima qilib beraman.\n\n"
        "Hi! Send me a message in Uzbek, English or Russian — "
        "I will translate it into the other two languages.\n\n"
        "Привет! Отправьте сообщение на узбекском, английском или "
        "русском — я переведу его на два других языка."
    )
    await update.message.reply_text(text)


async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    source_lang = detect_language(text)
    targets = [lang for lang in TARGET_LANGS if lang != source_lang]

    reply_lines = [f"Aniqlangan til / Detected: {LANG_NAMES.get(source_lang, source_lang)}\n"]

    for target in targets:
        try:
            translated = GoogleTranslator(source=source_lang, target=target).translate(text)
        except Exception as e:
            logger.error(f"Tarjima xatosi ({source_lang}->{target}): {e}")
            translated = "⚠️ Tarjima qilishda xatolik yuz berdi."

        reply_lines.append(f"{LANG_NAMES.get(target, target)}:\n{translated}\n")

    await update.message.reply_text("\n".join(reply_lines))


def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable topilmadi. "
            "Uni serverda o'rnating, masalan:\n"
            "export BOT_TOKEN='sizning_tokeningiz'"
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
