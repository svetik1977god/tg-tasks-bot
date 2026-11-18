"""
Обработчик команды /list_csv — отправка задач файлом CSV.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

from database.db import get_all_tasks
from utils.csv_export import tasks_to_csv

router = Router(name="list_csv")


@router.message(Command("list_csv"))
async def cmd_list_csv(message: Message) -> None:
    """
    Формирует CSV-файл со всеми задачами и отправляет его пользователю.
    """
    tasks = get_all_tasks()

    if not tasks:
        await message.answer("Список задач пуст. Добавьте задачу командой /add")
        return

    # Получаем готовый файл в памяти
    csv_buffer = tasks_to_csv(tasks)

    # BufferedInputFile говорит aiogram: "это файл, отправь его как документ"
    document = BufferedInputFile(
        file=csv_buffer.getvalue(),
        filename="tasks.csv",
    )

    await message.answer_document(
        document=document,
        caption=f"📄 Задачи в CSV (всего: {len(tasks)})",
    )
