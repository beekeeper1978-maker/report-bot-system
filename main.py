import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_ _name_ _)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает! Привет!")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Тест пройден!")

def main():
    print("=" * 50)
    print("🤖 БОТ ЗАПУСКАЕТСЯ")
    print("=" * 50)
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    
    print("Бот запущен!")
    app.run_polling()

if name == "_ _main_ _":
    main()
