import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8446705525:AAH8evf1zy3QXKj-fJh2cc_KdM-OA2rFaBw")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://script.google.com/macros/s/AKfycbwdxFdnC_9uEVPdjxkCUSKROYIlQ-AO5nyZPX6wXR-I1OSLiesXBoDHj-nY4rGw9TQqqA/exec")

QUESTIONS = [
"1. Отчётный период (например: 10-16 марта 2025)",
"2. Автор отчёта (ФИО)",
"3. Подразделение",
"4. Ключевые результаты недели (по пунктам)",
"5. Что проверено по чек-листу аудита",
"6. Номера задач в Битрикс24",
"7. Финансы (куплено/отремонтировано)",
"8. Пункты KPI, требующие внимания",
"9. План на следующую неделю"
]

Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, FINISH = range(10)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("Привет! Я бот для отчетов. Напиши /report чтобы начать")
return ConversationHandler.END

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
context.user_data["answers"] = []
await update.message.reply_text(f"{QUESTIONS[0]}")
return Q1

async def handle_q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[1]}")
return Q2

async def handle_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[2]}")
return Q3

async def handle_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[3]}")
return Q4

async def handle_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[4]}")
return Q5

async def handle_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[5]}")
return Q6

async def handle_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[6]}")
return Q7

async def handle_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[7]}")
return Q8

async def handle_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[8]}")
return Q9

async def handle_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text("Все вопросы пройдены! Напиши 'готово' чтобы отправить отчет")
return FINISH

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_data = context.user_data
try:
if len(user_data["answers"]) < 9:
await update.message.reply_text("Не все вопросы отвечены")
return ConversationHandler.END
data = {
"user_id": str(update.effective_user.id),
"period": user_data["answers"][0],
"author": user_data["answers"][1],
"department": user_data["answers"][2],
"key_results": user_data["answers"][3],
"audit_checklist": user_data["answers"][4],
"bitrix_tasks": user_data["answers"][5],
"finances": user_data["answers"][6],
"kpi_attention": user_data["answers"][7],
"next_week_plan": user_data["answers"][8]
}
response = requests.post(WEBHOOK_URL, json=data)
if response.status_code == 200:
await update.message.reply_text("Отчет отправлен в Google Таблицу!")
else:
await update.message.reply_text("Ошибка отправки")
except Exception as e:
await update.message.reply_text(f"Ошибка: {str(e)}")
context.user_data.clear()
return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("Отчет отменен")
context.user_data.clear()
return ConversationHandler.END

def main():
print("Запускаю бота...")
try:
app = Application.builder().token(BOT_TOKEN).build()
conv_handler = ConversationHandler(
entry_points=[CommandHandler("report", report)],
states={
Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q1)],
Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q2)],
Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q3)],
Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q4)],
Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q5)],
Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q6)],
Q7: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q7)],
Q8: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q8)],
Q9: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q9)],
FINISH: [MessageHandler(filters.TEXT & filters.Regex("^(готово)$"), finish)]
},
fallbacks=[CommandHandler("cancel", cancel)]
)
app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)
print("Бот запущен!")
app.run_polling()
except Exception as e:
print(f"Ошибка: {e}")

if __name__ == "__main__":
main()
