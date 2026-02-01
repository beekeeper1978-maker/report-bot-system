")
    
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
        'plan': data['answers'][8] if len(data['answers']) > 8 else '',
        'photos': data['photos'],
        'captions': data['captions']
    }
    
    try:
        response = requests.post(GOOGLE_URL, json=report_data, timeout=10)
        logger.info(f"Отправка в Google: статус {response.status_code}")
        
        if response.status_code == 200:
            await update.message.reply_text(
                "🎉 ОТЧЕТ СОХРАНЕН!\n\n"
                "Все данные записаны в Google Таблицу."
            )
        else:
            await update.message.reply_text(f"⚠️ Ошибка: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("❌ Ошибка соединения с Google")
    
    if user_id in user_data:
        del user_data[user_id]

def main():
    logger.info("🤖 БОТ ЗАПУЩЕН")
    print("🤖 БОТ ЗАПУЩЕН")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    logger.info("✅ Бот готов к работе")
    print("✅ Бот готов к работе")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

main()
