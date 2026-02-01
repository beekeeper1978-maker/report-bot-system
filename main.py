import os
import logging
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw"
GOOGLE_URL = "https://script.google.com/macros/s/AKfycbw3FYa8iJ-FrDHSnL8vvecHvYr2bZ_sk_W3owJbhuLD756JEsBIMWJO1IxHAuHbh-6JkA/exec"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUESTIONS = [
"1. 📅 Отчётный период (например, 01-07 февраля 2025):",
"2. 👤 Автор отчёта (ФИО):",
"3. 🏢 Подразделение:",
"4. 🎯 Ключевые результаты недели:",
"5. ✅ Что проверено по чек-листу аудита:",
"6. 📋 Номера задач в Битрикс24:",
"7. 💰 Финансы (куплено/отремонтировано):",
"8. ⚠️ Пункты KPI, требующие внимания:",
"9. 📈 План на следующую неделю:"
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
"📊 Бот для еженедельных отчетов\n\n"
"Напиши /report чтобы начать новый отчет"
)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id

user_data[user_id] = {
'step': 0,
'answers': [],
'start_time': datetime.now()
}

await update.message.reply_text(
"📝 НАЧИНАЕМ СОЗДАНИЕ ОТЧЕТА\n\n"
f"{QUESTIONS[0]}\n\n"
"Напиши ответ:"
)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id
text = update.message.text.strip()

if text.startswith('/'):
return

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
"🎉 ВСЕ ВОПРОСЫ ПРОЙДЕНЫ!\n\n"
"Теперь отправь фото (если нужно) или напиши 'готово' чтобы сохранить отчет.\n\n"
"📸 Можно отправить до 6 фото\n"
"🏷️ После каждого фото напиши подпись\n"
"✅ Напиши 'готово' для сохранения"
)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id

if user_id not in user_data:
await update.message.reply_text("Сначала начни отчет /report")
return

data = user_data[user_id]

if data['step'] < len(QUESTIONS):
await update.message.reply_text("Сначала ответь на все вопросы")
return

await update.message.reply_text(
"📸 Фото получено!\n"
"Напиши подпись к этому фото:"
)

async def finish_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_id = update.effective_user.id
text = update.message.text.strip().lower()

if text != 'готово':
return

if user_id not in user_data:
await update.message.reply_text("Сначала начни отчет /report")
return

data = user_data[user_id]

if data['step'] < len(QUESTIONS):
await update.message.reply_text("Сначала ответь на все вопросы")
return

await update.message.reply_text("⏳ Сохраняю отчет в Google Таблицу...")

report_data = {
'user_id': str(user_id),
'timestamp': data['start_time'].isoformat(),
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
await update.message.reply_text(
"✅ ОТЧЕТ УСПЕШНО СОХРАНЕН!\n\n"
"Все данные записаны в Google Таблицу.\n"
"Скоро получишь презентацию."
)
else:
await update.message.reply_text(f"⚠️ Ошибка сохранения: {response.status_code}")

except Exception as e:
logger.error(f"Ошибка: {e}")
await update.message.reply_text("❌ Ошибка соединения с Google")

if user_id in user_data:
del user_data[user_id]

def main():
print("=" * 50)
print("🤖 БОТ ДЛЯ ОТЧЕТОВ ЗАПУЩЕН")
print("=" * 50)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("report", report))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex('готово'), finish_report))

print("✅ Бот готов к сбору отчетов!")
app.run_polling()

main()
