import os

QUESTIONS = [
    "Отчётный период (например, 01-07 февраля 2025):",
    "Автор отчёта (ФИО):",
    "Подразделение:",
    "Ключевые результаты недели:",
    "Что проверено по чек-листу аудита:",
    "Номера задач в Битрикс24:",
    "Финансы (куплено/отремонтировано):",
    "Пункты KPI, требующие внимания:",
    "План на следующую неделю:"
]

MAX_PHOTOS = 6
GOOGLE_URL = os.getenv("WEBHOOK_URL", "https://script.google.com/macros/s/AKfycbw3FYa8iJ-FrDHSnL8vvecHvYr2bZ_sk_W3owJbhuLD756JEsBIMWJO1IxHAuHbh-6JkA/exec")
