"""
Точка входа: запуск Telegram-бота.

Запуск:
    python main.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.db import init_db
from handlers import add, list_csv, list_tasks, start


async def main() -> None:
    """
    Главная функция: настраивает бота и запускает его.
    """
    if not BOT_TOKEN:
        raise SystemExit(
            "Не найден BOT_TOKEN.\n"
            "Скопируйте .env.example в .env и вставьте токен от @BotFather."
        )

    # Логи помогают видеть, что происходит, в консоли
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Создаём таблицу в базе данных при старте
    init_db()

    # Bot — сам бот, Dispatcher — "мозг", который распределяет сообщения
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Подключаем роуты (наборы обработчиков) к диспетчеру.
    # Порядок важен: /list_csv должен идти раньше /list,
    # иначе /list может перехватить команду.
    dp.include_router(start.router)
    dp.include_router(add.router)
    dp.include_router(list_csv.router)
    dp.include_router(list_tasks.router)

    try:
        # Пропускаем накопившиеся сообщения и начинаем принимать новые
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # Аккуратно закрываем сессию бота
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as error:
        if str(error):
            print(error)
