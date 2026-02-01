import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает! Команда /start")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Команда /report работает! Отчет начат")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Команда /test работает!")

def main():
    print("🤖 Бот запускается...")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("test", test))
    
    print("✅ Бот запущен!")
    app.run_polling()

main()
