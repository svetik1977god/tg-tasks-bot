"""
Обработчик команды /start.
"""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.menu import main_menu

# Router — это "набор обработчиков". В main.py мы подключим его к боту.
router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Отвечает на /start приветствием и показывает кнопки меню.
    """
    await message.answer(
        "Привет! 👋\n"
        "Я бот для командной работы над задачами.\n\n"
        "Что я умею:\n"
        "/add &lt;текст&gt; — добавить задачу\n"
        "/list — показать все задачи\n"
        "/list_csv — скачать список задач в CSV\n\n"
        "Можно просто нажать кнопку ниже 👇",
        reply_markup=main_menu(),
    )
