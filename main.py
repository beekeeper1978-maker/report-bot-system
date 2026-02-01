import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from config import BOT_TOKEN, WEBHOOK_URL, QUESTIONS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, PHOTO, FINISH = range(11)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("Привет! Я бот для отчетов. Напиши /report чтобы начать")
return ConversationHandler.END

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
context.user_data["answers"] = []
context.user_data["photos"] = []

await update.message.reply_text(f"{QUESTIONS[0]}\n\n(напиши ответ текстом)")
return Q1

async def handle_q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[1]}\n\n(напиши ответ текстом)")
return Q2

async def handle_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[2]}\n\n(напиши ответ текстом)")
return Q3

async def handle_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[3]}\n\n(напиши ответ текстом)")
return Q4

async def handle_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[4]}\n\n(напиши ответ текстом)")
return Q5

async def handle_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[5]}\n\n(напиши ответ текстом)")
return Q6

async def handle_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[6]}\n\n(напиши ответ текстом)")
return Q7

async def handle_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[7]}\n\n(напиши ответ текстом)")
return Q8

async def handle_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)
await update.message.reply_text(f"{QUESTIONS[8]}\n\n(напиши ответ текстом)")
return Q9

async def handle_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data["answers"].append(update.message.text)

await update.message.reply_text(
"✅ Все вопросы пройдены!\n\n"
"📸 Теперь можно добавить фото (необязательно)\n"
"Отправь фото или напиши 'готово' чтобы закончить"
)
return PHOTO

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.photo:
photo = update.message.photo[-1]
context.user_data["photos"].append(photo.file_id)
await update.message.reply_text(f"✅ Фото сохранено. Можно добавить еще фото или написать 'готово'")
return PHOTO

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_data = context.user_data

try:
data = {
"period": user_data["answers"][0] if len(user_data["answers"]) > 0 else "",
"author": user_data["answers"][1] if len(user_data["answers"]) > 1 else "",
"department": user_data["answers"][2] if len(user_data["answers"]) > 2 else "",
"results": user_data["answers"][3] if len(user_data["answers"]) > 3 else "",
"problems": user_data["answers"][4] if len(user_data["answers"]) > 4 else "",
"solved": user_data["answers"][5] if len(user_data["answers"]) > 5 else "",
"help": user_data["answers"][6] if len(user_data["answers"]) > 6 else "",
"rating": user_data["answers"][7] if len(user_data["answers"]) > 7 else "",
"plan": user_data["answers"][8] if len(user_data["answers"]) > 8 else "",
"photos_count": len(user_data["photos"]),
"chat_id": update.effective_chat.id
}

response = requests.post(WEBHOOK_URL, json=data)

if response.status_code == 200:
await update.message.reply_text("🎉 Отчет отправлен в Google Таблицу!")
else:
await update.message.reply_text("⚠️ Данные собраны, но ошибка отправки в Google")

except Exception as e:
await update.message.reply_text(f"❌ Ошибка: {str(e)}")

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
PHOTO: [
MessageHandler(filters.PHOTO, handle_photo),
MessageHandler(filters.TEXT & filters.Regex("^(готово|закончить)$"), finish)
]
},
fallbacks=[CommandHandler("cancel", cancel)]
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)

print("Бот запущен!")
app.run_polling()

except Exception as e:
print(f"Ошибка: {e}")

if name == "main":
main()
