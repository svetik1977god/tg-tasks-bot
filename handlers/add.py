"""
Обработчик команды /add — добавление задачи.

Работает двумя способами:
1) /add Купить хлеб      — задача берётся из самой команды;
2) /add                  — бот ждёт следующее сообщение с текстом задачи.
"""

from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.db import add_task

router = Router(name="add")


class AddTask(StatesGroup):
    """
    Состояния (шаги) диалога добавления задачи.
    """

    waiting_for_text = State()  # ждём текст задачи от пользователя


@router.message(Command("add"))
async def cmd_add(
    message: Message, command: CommandObject, state: FSMContext
) -> None:
    """
    Если текст написан сразу после /add — сохраняем его.
    Если текста нет — переводим бота в режим ожидания текста.
    """
    task_text = (command.args or "").strip()

    if task_text:
        await _save_and_reply(message, task_text)
        return

    # Текста в команде нет — просим написать задачу следующим сообщением
    await state.set_state(AddTask.waiting_for_text)
    await message.answer("Напишите текст задачи одним сообщением:")


@router.message(AddTask.waiting_for_text, F.text)
async def process_task_text(message: Message, state: FSMContext) -> None:
    """
    Получаем текст задачи, сохраняем его и выходим из режима ожидания.
    """
    # Если пользователь передумал и отправил другую команду — не сохраняем её
    if message.text.startswith("/"):
        await state.clear()
        await message.answer("Добавление задачи отменено. Выберите команду из меню.")
        return

    await state.clear()
    await _save_and_reply(message, message.text.strip())


async def _save_and_reply(message: Message, task_text: str) -> None:
    """
    Общая часть: сохраняет задачу в базу и отвечает пользователю.
    """
    if not task_text:
        await message.answer("Задача не может быть пустой.")
        return

    # Имя пользователя: @username, а если его нет — имя из профиля
    user_name = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else message.from_user.full_name
    )

    task_id = add_task(task_text, user_name)
    # Текст задачи экранируем: иначе символы < и > Telegram примет за HTML-теги
    await message.answer(f"✅ Задача #{task_id} добавлена:\n{escape(task_text)}")
