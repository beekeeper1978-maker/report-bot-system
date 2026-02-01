import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("БОТ РАБОТАЕТ! Команда /start")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("БОТ РАБОТАЕТ! Команда /report")

def main():
    print("=" * 50)
    print("🤖 ЗАПУСКАЮ БОТА")
    print("=" * 50)
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    
    print("✅ Бот запущен!")
    print("📱 Ожидаю сообщения...")
    
    app.run_polling()

main()
