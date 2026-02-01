import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройки
TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Простая команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает! Привет!")

# Команда /test
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Тест пройден! Бот отвечает!")

# Главная функция
def main():
    print("=" * 50)
    print("🚀 ЗАПУСК ПРОСТОГО БОТА ДЛЯ ТЕСТА")
    print(f"Токен: {TOKEN[:20]}...")
    print("=" * 50)
    
    app = Application.builder().token(TOKEN).build()
    
    # Только 2 команды для теста
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    
    print("🤖 Бот запускается...")
    app.run_polling()
    print("✅ Бот работает!")

if name == "__main__":
    main()
