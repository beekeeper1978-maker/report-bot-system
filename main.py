print("=== БОТ ЗАПУЩЕН ===")

import os
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")
print(f"Токен: {BOT_TOKEN[:10]}...")

async def start(update, context):
    await update.message.reply_text("✅ Бот работает!")

async def test(update, context):
    await update.message.reply_text("✅ Тестовая команда работает")

# Создаем бота
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("test", test))

print("Бот запущен!")
app.run_polling()
