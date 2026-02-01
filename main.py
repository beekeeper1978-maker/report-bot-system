import os
import logging
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")
GOOGLE_URL = os.getenv("WEBHOOK_URL", "https://script.google.com/macros/s/AKfycbw3FYa8iJ-FrDHSnL8vvecHvYr2bZ_sk_W3owJbhuLD756JEsBIMWJO1IxHAuHbh-6JkA/exec")

# Включим подробное логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Вопросы
QUESTIONS = [
    "📅 1. Отчётный период (например, 01-07 февраля 2025):",
    "👤 2. Автор отчёта (ФИО):", 
    "🏢 3. Подразделение:",
    "🎯 4. Ключевые результаты недели:",
    "🔍 5. Что проверено по чек-листу аудита:",
    "📋 6. Номера задач в Битрикс24:",
    "💰 7. Финансы (куплено/отремонтировано):",
    "📊 8. Пункты KPI, требующие внимания:",
    "📝 9. План на следующую неделю:"
]

# Хранилище данных пользователей
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.full_name}) вызвал /start")
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Я бот для сбора еженедельных отчетов.\n\n"
        "📋 **Доступные команды:**\n"
        "/report - начать новый отчет\n"
        "/cancel - отменить текущий отчет\n"
        "/help - показать справку"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "ℹ️ **Справка по боту:**\n\n"
        "1. Напиши /report чтобы начать отчет\n"
        "2. Отвечай на вопросы по порядку\n"
        "3. Можно отправлять фото с подписями\n"
        "4. Напиши 'готово' для завершения\n\n"
        "🔄 /cancel - отменить отчет\n"
        "❓ /help - эта справка"
    )

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /report"""
    user_id = update.effective_user.id
    logger.info(f"Пользователь {user_id} начал новый отчет")
    
    # Создаем новую сессию
    user_data[user_id] = {
        'step': 0,           # Текущий вопрос
        'answers': [],       # Ответы на вопросы
        'photos': [],        # ID фото
        'captions': [],      # Подписи к фото
        'start_time': datetime.now(),
        'waiting_caption': None  # Индекс фото, для которого ждем подпись
    }
    
    # Задаем первый вопрос
    await update.message.reply_text(
        "📋 **НАЧИНАЕМ НОВЫЙ ОТЧЕТ**\n\n"
        f"{QUESTIONS[0]}\n\n"
        "✍️ Напиши ответ ниже:"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /cancel"""
    user_id = update.effective_user.id
    
    if user_id in user_data:
        del user_data[user_id]
        await update.message.reply_text(
            "🗑️ **Отчет отменен**\n"
            "Все данные удалены.\n\n"
            "Напиши /report чтобы начать заново."
        )
    else:
        await update.message.reply_text(
            "ℹ️ У вас нет активного отчета.\n"
            "Напиши /report чтобы начать."
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    logger.info(f"Пользователь {user_id} отправил текст: {text}")
    
    # Проверяем, начал ли пользователь отчет
    if user_id not in user_data:
        await update.message.reply_text(
            "❓ **Сначала начни отчет!**\n\n"
            "Напиши команду /report чтобы начать."
        )
        return
    
    data = user_data[user_id]
    
    # Если ждем подпись к фото
    if data['waiting_caption'] is not None:
        idx = data['waiting_caption']
        data['captions'][idx] = text
        data['waiting_caption'] = None
await update.message.reply_text(
            f"✅ **Подпись сохранена!**\n"
            f"📸 Фото {len(data['photos'])}\n\n"
            "Можешь отправить еще фото или напиши 'готово' для завершения."
        )
        return
    
    # Если пользователь пишет 'готово'
    if text.lower() == 'готово':
        if data['step'] < len(QUESTIONS):
            await update.message.reply_text(
                "⚠️ **Сначала ответь на все вопросы!**\n\n"
                f"Осталось ответить на {len(QUESTIONS) - data['step']} вопросов."
            )
        else:
            await save_report(update, user_id)
        return
    
    # Если отвечаем на вопросы
    if data['step'] < len(QUESTIONS):
        # Сохраняем ответ
        data['answers'].append(text)
        data['step'] += 1
        
        logger.info(f"Пользователь {user_id} ответил на вопрос {data['step']}/{len(QUESTIONS)}")
        
        # Если остались вопросы
        if data['step'] < len(QUESTIONS):
            await update.message.reply_text(
                f"✅ **Ответ сохранен!**\n\n"
                f"{QUESTIONS[data['step']]}\n\n"
                "✍️ Напиши ответ ниже:"
            )
        else:
            # Все вопросы пройдены
            await update.message.reply_text(
                "🎉 **ВСЕ ВОПРОСЫ ПРОЙДЕНЫ!**\n\n"
                "Теперь можно отправить фото.\n\n"
                "📸 **Как отправлять фото:**\n"
                "1. Нажми на скрепку 📎\n"
                "2. Выбери 'Фото или видео'\n"
                "3. Выбери фото\n"
                "4. После фото напиши подпись\n\n"
                "📎 Можно отправить до 10 фото.\n"
                "✅ Когда закончишь, напиши 'готово'"
            )
    else:
        # Уже ответили на все вопросы, но не фото этап
        await update.message.reply_text(
            "📸 **Отправь фото или напиши 'готово'**\n\n"
            "Нажми на скрепку 📎 чтобы отправить фото."
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик фото"""
    user_id = update.effective_user.id
    
    logger.info(f"Пользователь {user_id} отправил фото")
    
    if user_id not in user_data:
        await update.message.reply_text(
            "❓ **Сначала начни отчет!**\n\n"
            "Напиши команду /report чтобы начать."
        )
        return
    
    data = user_data[user_id]
    
    # Проверяем, что ответили на все вопросы
    if data['step'] < len(QUESTIONS):
        await update.message.reply_text(
            f"⚠️ **Сначала ответь на вопросы!**\n\n"
            f"Осталось ответить на {len(QUESTIONS) - data['step']} вопросов."
        )
        return
    
    # Получаем фото (самый большой размер)
    photo = update.message.photo[-1]
    file_id = photo.file_id
    
    # Сохраняем фото
    data['photos'].append(file_id)
    data['captions'].append('')  # Пустая подпись пока что
    
    # Просим подпись
    data['waiting_caption'] = len(data['photos']) - 1
    
    await update.message.reply_text(
        f"📸 **Фото {len(data['photos'])} получено!**\n\n"
        "✍️ **Напиши подпись к этому фото:**\n"
        "(Опиши что на фото, или для чего оно)"
    )

async def save_report(update: Update, user_id: int):
    """Сохранение отчета в Google Таблицу"""
    data = user_data[user_id]
    
    logger.info(f"Сохранение отчета для пользователя {user_id}")
    
    # Показываем статус
    await update.message.reply_text(
        "⏳ **СОХРАНЯЕМ ОТЧЕТ...**\n\n"
        "Отправляю данные в Google Таблицу..."
    )
    
    # Подготавливаем данные для Google
    report_data = {
        'user_id': str(user_id),
        'timestamp': data['start_time'].isoformat(),
        'period': data['answers'][0] if len(data['answers']) > 0 else '',
        'author': data['answers'][1] if len(data['answers']) > 1 else '',
        'department': data['answers'][2] if len(data['answers]) > 2 else '',
        'key_results': data['answers'][3] if len(data['answers']) > 3 else '',
        'audit': data['answers'][4] if len(data['answers']) > 4 else ‘',
'bitrix': data['answers'][5] if len(data['answers']) > 5 else '',
        'finances': data['answers'][6] if len(data['answers']) > 6 else '',
        'kpi': data['answers'][7] if len(data['answers']) > 7 else '',
        'plan': data['answers'][8] if len(data['answers']) > 8 else '',
        'photos': data['photos'],
        'captions': data['captions']
    }
    
    try:
        # Отправляем в Google
        logger.info(f"Отправка данных в Google: {report_data}")
        response = requests.post(GOOGLE_URL, json=report_data, timeout=30)
        
        logger.info(f"Ответ от Google: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            await update.message.reply_text(
                "✅ **ОТЧЕТ УСПЕШНО СОХРАНЕН!**\n\n"
                "Все данные записаны в Google Таблицу.\n\n"
                "📊 Таблица: https://docs.google.com/spreadsheets/d/1fGLUGhNDwyNps4VnsdOleOFb4YdJQOIn5B1jSVmJilM/edit\n\n"
                "🔄 Напиши /report чтобы начать новый отчет."
            )
        else:
            await update.message.reply_text(
                f"⚠️ **ОШИБКА СОХРАНЕНИЯ**\n\n"
                f"Код ошибки: {response.status_code}\n"
                f"Ответ: {response.text}\n\n"
                "Попробуй позже или свяжись с администратором."
            )
            
    except requests.exceptions.Timeout:
        logger.error("Таймаут при отправке в Google")
        await update.message.reply_text(
            "⏰ **ТАЙМАУТ СОЕДИНЕНИЯ**\n\n"
            "Google не ответил вовремя.\n"
            "Попробуй сохранить отчет позже."
        )
    except Exception as e:
        logger.error(f"Ошибка при сохранении: {e}")
        await update.message.reply_text(
            f"❌ **КРИТИЧЕСКАЯ ОШИБКА**\n\n"
            f"Ошибка: {str(e)}\n\n"
            "Сообщи об ошибке администратору."
        )
    
    # Удаляем данные пользователя
    if user_id in user_data:
        del user_data[user_id]

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка в боте: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ **Произошла ошибка**\n\n"
            "Попробуй еще раз или напиши /start"
        )

def main():
    """Основная функция"""
    print("=" * 50)
    print("🤖 БОТ ДЛЯ ОТЧЕТОВ ЗАПУСКАЕТСЯ")
    print(f"Токен: {'OK' if TOKEN else 'НЕТ ТОКЕНА!'}")
    print(f"Google URL: {GOOGLE_URL}")
    print("=" * 50)
    
    try:
        # Создаем приложение
        app = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики команд
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("report", report))
        app.add_handler(CommandHandler("cancel", cancel))
        app.add_handler(CommandHandler("help", help_command))
        
        # Добавляем обработчики сообщений
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        # Добавляем обработчик ошибок
        app.add_error_handler(error_handler)
        
        print("✅ Бот запущен и готов к работе!")
        print("Ожидаю сообщения...")
        print("=" * 50)
        
        # Запускаем бота
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА ПРИ ЗАПУСКЕ: {e}")
        logger.error(f"Ошибка запуска: {e}")

if name == "__main__":
    main()
