"""
Настройки проекта.

Токен бота берётся из файла .env (переменная BOT_TOKEN).
Скопируйте .env.example в .env и вставьте туда свой токен от @BotFather.
"""

import os

from dotenv import load_dotenv

# Читаем переменные из файла .env (если он есть рядом с main.py)
load_dotenv()

# Токен Telegram-бота. Получить можно у @BotFather в Telegram.
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Путь к файлу базы данных SQLite.
# Если файла нет, он создастся автоматически при первом запуске.
DB_PATH = os.getenv("DB_PATH", "tasks.db")
