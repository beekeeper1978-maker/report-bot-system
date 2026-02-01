// === КОНФИГУРАЦИЯ ===
var SPREADSHEET_ID = '1T6DS5eK1yMeXCLX-ft0NqUFSRtcsHUonoIDBWJRWzGA';

// === ОСНОВНАЯ ФУНКЦИЯ ДЛЯ ПРИЁМА ДАННЫХ ===
function doPost(e) {
  try {
    // Открываем таблицу
    var spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheet = spreadsheet.getActiveSheet();
    
    // Получаем данные от бота
    var data = JSON.parse(e.postData.contents);
    
    // Создаём новую строку с данными
    var newRow = [
      new Date(),                           // Время получения
      data.user_id || '',                  // ID пользователя
      data.period || '',                   // Отчётный период
      data.author || '',                   // Автор отчёта
      data.department || '',               // Подразделение
      data.key_results || '',              // Ключевые результаты
      data.audit_checklist || '',          // Чек-лист аудита
      data.bitrix_tasks || '',             // Задачи Битрикс24
      data.finances || '',                 // Финансы
      data.kpi_attention || '',            // KPI для внимания
      data.next_week_plan || ''            // План на неделю
    ];
    
    // Добавляем 12 пустых колонок для фото (6 фото + 6 подписей)
    for (var i = 0; i < 12; i++) {
      newRow.push('');
    }
    
    // Добавляем строку в таблицу
    sheet.appendRow(newRow);
    
    // Возвращаем успешный ответ
    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'Данные сохранены в строку ' + sheet.getLastRow(),
      row_number: sheet.getLastRow()
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Возвращаем ошибку
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// === ФУНКЦИЯ ДЛЯ ПРОВЕРКИ РАБОТЫ СКРИПТА ===
function doGet() {
  return HtmlService.createHtmlOutput(
    '<h1 style="color: green;">✅ Google Script для бота работает!</h1>' +
    '<p>Система готова принимать данные от Telegram-бота.</p>'
  );
}

// === ТЕСТОВАЯ ФУНКЦИЯ ===
function testAddRow() {
  var sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getActiveSheet();
  
  sheet.appendRow([
    new Date(),
    'TEST_USER',
    'ТЕСТОВЫЙ ПЕРИОД',
    'ТЕСТОВЫЙ АВТОР',
    'ТЕСТОВОЕ ПОДРАЗДЕЛЕНИЕ',
    'Тестовые результаты',
    'Тестовый чек-лист',
    'B24-001, B24-002',
    'Тестовые финансы',
    'Тестовый KPI',
    'Тестовый план'
  ]);
  
  return 'Тестовая запись добавлена в строку ' + sheet.getLastRow();
}
