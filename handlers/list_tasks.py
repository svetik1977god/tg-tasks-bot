"""
Обработчик команды /list — вывод всех задач текстом.
"""

from html import escape

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.db import get_all_tasks

router = Router(name="list")

# Telegram не принимает сообщения длиннее 4096 символов,
# поэтому режем длинный список на несколько сообщений.
MAX_MESSAGE_LENGTH = 4000


@router.message(Command("list"))
async def cmd_list(message: Message) -> None:
    """
    Показывает все задачи из базы.
    """
    tasks = get_all_tasks()

    if not tasks:
        await message.answer("Список задач пуст. Добавьте задачу командой /add")
        return

    # Собираем строки вида "1. [user] текст (дата)"
    # escape() нужен, чтобы < и > в задачах не ломали HTML-разметку сообщения
    lines = [
        f"{task['id']}. {escape(task['text'])} — {escape(task['user'])} ({task['created_at']})"
        for task in tasks
    ]

    header = f"📋 Всего задач: {len(tasks)}\n\n"
    await _send_long_text(message, header + "\n".join(lines))


async def _send_long_text(message: Message, text: str) -> None:
    """
    Отправляет длинный текст частями, чтобы не превысить лимит Telegram.
    """
    for start in range(0, len(text), MAX_MESSAGE_LENGTH):
        await message.answer(text[start : start + MAX_MESSAGE_LENGTH])
