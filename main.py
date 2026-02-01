import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")
GOOGLE_URL = os.getenv("WEBHOOK_URL", "https://script.google.com/macros/s/AKfycbzzkwX4skSmvgEA0ljxU9sLvNFwZOi-LF1tBR4NYg1-U_jY1GoaFDoj_isY5_hQG2YgrQ/exec")

# === ЛОГГИРОВАНИЕ ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === КОМАНДА /start ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "✅ **Бот для еженедельных отчётов запущен!**\n\n"
        "Используйте /start_report чтобы начать новый отчёт."
    )

# === КОМАНДА /start_report ===
async def start_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📋 **Начинаем создание отчёта:**\n\n"
        "1. Введите отчётный период (например, 01-07 февраля 2025):"
    )

# === ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ ===
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = update.effective_user.id
    
    # Логируем полученное сообщение
    logger.info(f"Пользователь {user_id} отправил: {text}")
    
    # Отправляем подтверждение пользователю
    await update.message.reply_text(f"📝 Получено: {text}")
    
    try:
        # Подготовка данных для отправки в Google
        payload = {
            "user_id": user_id,
            "period": text,  # Пока отправляем только период
            "timestamp": "2025-01-01"  # Заглушка для теста
        }
        
        # Отправка в Google Скрипт
        response = requests.post(GOOGLE_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            await update.message.reply_text("✅ Данные успешно сохранены в Google Таблицу!")
        else:
            await update.message.reply_text("⚠️ Ошибка при сохранении данных.")
            
    except Exception as error:
        logger.error(f"Ошибка отправки: {error}")
        await update.message.reply_text("❌ Ошибка соединения с Google.")

# === ОБРАБОТКА ОШИБОК ===
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Ошибка в боте: {context.error}")

# === ОСНОВНАЯ ФУНКЦИЯ ===
def main() -> None:
    """Запуск бота"""
    
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("start_report", start_report_command))
    
    # Добавление обработчика текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Добавление обработчика ошибок
    application.add_error_handler(error_handler)
    
    # Запуск бота
    logger.info("Бот запускается...")
    print("=" * 60)
    print("🤖 БОТ ДЛЯ ОТЧЁТОВ ЗАПУЩЕН")
    print("📅 Версия: 1.0")
    print("🐍 Python: 3.9 (совместим с Railway)")
    print("=" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# === ТОЧКА ВХОДА ===
if name == "__main__":
    main()
