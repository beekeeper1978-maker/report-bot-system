import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")
GOOGLE_URL = os.getenv("WEBHOOK_URL", "https://script.google.com/macros/s/AKfycbw3FYa8iJ-FrDHSnL8vvecHvYr2bZ_sk_W3owJbhuLD756JEsBIMWJO1IxHAuHbh-6JkA/exec")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUESTIONS = [
"1. Отчётный период (например, 01-07 февраля 2025):",
"2. Автор отчёта (ФИО):",
"3. Подразделение:",
"4. Ключевые результаты недели:",
"5. Что проверено по чек-листу аудита:",
"6. Номера задач в Битрикс24:",
"7. Финансы (куплено/отремонтировано):",
"8. Пункты KPI, требующие внимания:",
"9. План на следующую неделю:"
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
"📋 Бот для еженедельных отчетов\n\n"
"Напиши /report чтобы начать новый отчет"
)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id

user_data[user_id] = {
'step': 0,
'answers': []
}

await update.message.reply_text(
"📝 НАЧИНАЕМ ОТЧЕТ\n\n"
f"{QUESTIONS[0]}\n\n"
"Напиши ответ:"
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id
text = update.message.text

logger.info(f"Пользователь {user_id}: {text}")

if user_id not in user_data:
return

data = user_data[user_id]

if data['step'] < len(QUESTIONS):
data['answers'].append(text)
data['step'] += 1

if data['step'] < len(QUESTIONS):
await update.message.reply_text(
f"✅ Ответ сохранен!\n\n"
f"{QUESTIONS[data['step']]}\n\n"
"Напиши ответ:"
)
else:
await update.message.reply_text(
"✅ Все вопросы пройдены!\n\n"
"Теперь отправь фото или напиши 'готово' чтобы завершить."
)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id

if user_id not in user_data:
await update.message.reply_text("Сначала напиши /report")
return

data = user_data[user_id]

if data['step'] < len(QUESTIONS):
await update.message.reply_text("Сначала ответь на все вопросы")
return

await update.message.reply_text(
"✅ Фото получено!\n\n"
"Можешь отправить еще фото или напиши 'готово' чтобы сохранить отчет."
)

async def finish_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id
text = update.message.text

if text.lower() != 'готово':
return

if user_id not in user_data:
await update.message.reply_text("Сначала напиши /report")
return

data = user_data[user_id]

if data['step'] < len(QUESTIONS):
await update.message.reply_text("Сначала ответь на все вопросы")
return

await update.message.reply_text("⏳ Сохраняю отчет в Google Таблицу...")

report_data = {
'user_id': str(user_id),
'period': data['answers'][0] if len(data['answers']) > 0 else '',
'author': data['answers'][1] if len(data['answers']) > 1 else '',
'department': data['answers'][2] if len(data['answers']) > 2 else '',
'key_results': data['answers'][3] if len(data['answers']) > 3 else '',
'audit': data['answers'][4] if len(data['answers']) > 4 else '',
'bitrix': data['answers'][5] if len(data['answers']) > 5 else '',
'finances': data['answers'][6] if len(data['answers']) > 6 else '',
'kpi': data['answers'][7] if len(data['answers']) > 7 else '',
'plan': data['answers'][8] if len(data['answers']) > 8 else ''
}

try:
response = requests.post(GOOGLE_URL, json=report_data, timeout=10)

if response.status_code == 200:
await update.message.reply_text("🎉 Отчет сохранен в Google Таблицу!")
else:
await update.message.reply_text(f"⚠️ Ошибка: {response.status_code}")

except Exception as e:
logger.error(f"Ошибка: {e}")
await update.message.reply_text("❌ Ошибка соединения с Google")

if user_id in user_data:
del user_data[user_id]

def main():
print("🤖 БОТ ЗАПУЩЕН")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("report", report))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.add_handler(MessageHandler(filters.TEXT & filters.Regex('готово'), finish_report))

print("✅ Бот готов к работе")
app.run_polling()

main()
