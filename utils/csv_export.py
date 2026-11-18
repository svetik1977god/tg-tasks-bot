"""
Превращение списка задач в CSV-файл.
"""

import csv
import io
import sqlite3


def tasks_to_csv(tasks: list[sqlite3.Row]) -> io.BytesIO:
    """
    Собирает CSV-файл из списка задач и возвращает его как поток байтов.

    BytesIO — это "файл в памяти": aiogram умеет отправлять такие объекты
    как документы, не сохраняя их на диск.
    """
    buffer = io.BytesIO()

    # newline="" — требование модуля csv, чтобы не появлялись пустые строки
    text_stream = io.StringIO(newline="")
    writer = csv.writer(text_stream, delimiter=";")

    # Заголовок таблицы
    writer.writerow(["id", "text", "user", "created_at"])

    # Сами задачи
    for task in tasks:
        writer.writerow([task["id"], task["text"], task["user"], task["created_at"]])

    # Кодировка utf-8-sig нужна, чтобы Excel правильно показал кириллицу
    buffer.write(text_stream.getvalue().encode("utf-8-sig"))
    buffer.seek(0)  # возвращаем "курсор" в начало файла
    return buffer
