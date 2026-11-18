"""
Работа с базой данных SQLite.

Таблица tasks:
    id         — уникальный номер задачи (заполняется автоматически)
    text       — текст задачи
    user       — имя пользователя, который добавил задачу
    created_at — дата и время добавления задачи
"""

import sqlite3
from datetime import datetime

from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """
    Открывает соединение с базой данных.

    sqlite3.connect создаст файл базы, если его ещё нет.
    row_factory = sqlite3.Row позволяет обращаться к полям строки по имени,
    например task["text"], а не task[1].
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """
    Создаёт таблицу tasks, если её ещё нет.
    Вызывается один раз при старте бота.
    """
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                user TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def add_task(text: str, user: str) -> int:
    """
    Добавляет новую задачу в базу.

    Возвращает id созданной задачи.
    """
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (text, user, created_at) VALUES (?, ?, ?)",
            (text, user, created_at),
        )
        # lastrowid — id только что добавленной строки
        return cursor.lastrowid


def get_all_tasks() -> list[sqlite3.Row]:
    """
    Возвращает все задачи, отсортированные по времени добавления.
    """
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT id, text, user, created_at FROM tasks ORDER BY id"
        )
        return cursor.fetchall()
