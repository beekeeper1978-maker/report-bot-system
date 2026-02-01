import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает! /start")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Начинаем отчет! /report")

def main():
    print("🚀 ЗАПУСКАЕМ БОТА...")
    
    try:
        app = Application.builder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("report", report))
        
        print("✅ Бот запущен!")
        print("🤖 Ожидаю команды...")
        
        app.run_polling()
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")

main()
