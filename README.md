# Telegram-бот для командной работы над задачами

Простой бот на `aiogram 3` + `SQLite3`: добавляет задачи в общий список,
показывает их и отправляет CSV-файл.

## Команды

| Команда | Что делает |
| --- | --- |
| `/start` | Приветствие и кнопки меню |
| `/add <текст>` | Добавить задачу (или просто `/add` и следующее сообщение) |
| `/list` | Показать все задачи |
| `/list_csv` | Получить CSV-файл со всеми задачами |

## Структура проекта

```
main.py               # точка входа, запуск бота
config.py             # токен и путь к базе (из .env)
database/
    db.py             # подключение к SQLite, таблица tasks, запросы
handlers/
    start.py          # /start
    add.py            # /add
    list_tasks.py     # /list
    list_csv.py       # /list_csv
keyboards/
    menu.py           # кнопки меню
utils/
    csv_export.py     # превращение задач в CSV
```

Таблица `tasks`: `id`, `text`, `user`, `created_at`.

## Установка и запуск

1. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Получите токен у [@BotFather](https://t.me/BotFather) и создайте файл `.env`:

```bash
copy .env.example .env
```

Вставьте токен в строку `BOT_TOKEN=...`.

3. Запустите бота:

```bash
python main.py
```

Файл базы `tasks.db` создастся автоматически при первом запуске.
