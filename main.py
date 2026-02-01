data['captions'].append('')
    
    data['waiting_caption'] = len(data['photos']) - 1
    await update.message.reply_text(f"📸 Фото {len(data['photos'])} получено! Напиши подпись:")

async def save_report(update: Update, user_id: int):
    data = user_data[user_id]
    
    # Подготовка данных
    report_data = {
        'user_id': user_id,
        'timestamp': data['start_time'].isoformat(),
        'period': data['answers'][0] if len(data['answers']) > 0 else '',
        'author': data['answers'][1] if len(data['answers']) > 1 else '',
        'department': data['answers'][2] if len(data['answers']) > 2 else '',
        'key_results': data['answers'][3] if len(data['answers']) > 3 else '',
        'audit': data['answers'][4] if len(data['answers']) > 4 else '',
        'bitrix': data['answers'][5] if len(data['answers']) > 5 else '',
        'finances': data['answers'][6] if len(data['answers']) > 6 else '',
        'kpi': data['answers'][7] if len(data['answers']) > 7 else '',
        'plan': data['answers'][8] if len(data['answers']) > 8 else '',
        'photos': data['photos'],
        'captions': data['captions']
    }
    
    await update.message.reply_text("⏳ Сохраняю отчет в Google Таблицу...")
    
    try:
        response = requests.post(GOOGLE_URL, json=report_data, timeout=10)
        
        if response.status_code == 200:
            await update.message.reply_text(
                "🎉 Отчет сохранен!\n"
                "Данные записаны в Google Таблицу."
            )
        else:
            await update.message.reply_text(f"⚠️ Ошибка: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("❌ Ошибка соединения с Google")
    
    # Удаляем данные
    if user_id in user_data:
        del user_data[user_id]

def main():
    print("=" * 50)
    print("🤖 БОТ ДЛЯ ОТЧЕТОВ ЗАПУЩЕН")
    print("=" * 50)
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Бот запущен и готов к работе!")
    app.run_polling()

main()
