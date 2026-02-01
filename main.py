'department': data['answers'][2] if len(data['answers']) > 2 else '',
        'key_results': data['answers'][3] if len(data['answers']) > 3 else '',
        'audit': data['answers'][4] if len(data['answers']) > 4 else '',
        'bitrix': data['answers'][5] if len(data['answers']) > 5 else '',
        'finances': data['answers'][6] if len(data['answers']) > 6 else '',
        'kpi': data['answers'][7] if len(data['answers']) > 7 else '',
        'plan': data['answers'][8] if len(data['answers']) > 8 else '',
        'photos': data['photos'],
        'photo_captions': data['photo_captions']
    }
    
    # Отправка в Google
    try:
        response = requests.post(GOOGLE_URL, json=google_data, timeout=10)
        
        if response.status_code == 200:
            await update.message.reply_text(
                "🎉 Отчет сохранен в Google Таблицу!\n"
                "Скоро бот отправит тебе презентацию."
            )
        else:
            await update.message.reply_text("Ошибка сохранения в Google")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка соединения с Google")
    
    # Удаляем данные пользователя
    del user_data[user_id]

# Главная функция
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", start_report))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Бот запущен!")
    app.run_polling()

if name == "__main__":
    main()
