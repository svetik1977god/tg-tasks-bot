"""
Клавиатуры бота.

ReplyKeyboardMarkup — это кнопки, которые появляются под полем ввода
вместо обычной клавиатуры телефона.
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    """
    Главное меню с кнопками для всех команд бота.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/add"), KeyboardButton(text="/list")],
            [KeyboardButton(text="/list_csv")],
        ],
        resize_keyboard=True,  # кнопки подстраиваются под размер экрана
    )
    return keyboard
