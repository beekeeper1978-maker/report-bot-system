import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Команда /start от пользователя {update.effective_user.id}")
    await update.message.reply_text("Бот работает! /start")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Команда /report от пользователя {update.effective_user.id}")
    await update.message.reply_text("Начинаем отчет! /report")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Команда /test от пользователя {update.effective_user.id}")
    await update.message.reply_text("Тест работает! /test")

def main():
    logger.info("=" * 50)
    logger.info("🚀 БОТ ЗАПУСКАЕТСЯ")
    logger.info("=" * 50)
    
    print("=" * 50)
    print("🚀 БОТ ЗАПУСКАЕТСЯ")
    print(f"Токен: {TOKEN[:20]}...")
    print("=" * 50)
    
    try:
        app = Application.builder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("report", report))
        app.add_handler(CommandHandler("test", test))
        
        logger.info("✅ Бот запущен и слушает команды")
        print("✅ Бот запущен и слушает команды")
        
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
        print(f"❌ Ошибка запуска бота: {e}")

main()
