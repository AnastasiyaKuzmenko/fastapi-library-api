# 📚 Library API

RESTful API для управления библиотечным каталогом с системой выдачи и возврата книг. Разработан с использованием FastAPI, SQLAlchemy, JWT-аутентификации и Alembic для миграций.

<!--
## Features
✅ Menu is rendered via a **custom template tag**.  
✅ All menu data is stored in the **database**.  
✅ Menus are editable via the **Django admin interface**.  
✅ **Multiple menus** can be rendered on a single page by name.  
✅ Each menu item supports a **URL or named URL pattern**.  
✅ The menu tree expands automatically to show the **active path**.  
✅ The **active item is highlighted** based on the current page.  
✅ Only **1 database query** is used per menu render. 
-->

## 📌 Структура проекта
```bash
.
├── .gitignore
│    
├── alembic/                # Миграции            
│    
├── app/                    
│   ├── auth.py             # JWT аутентификация
│   ├── database.py         # Подключение к БД 
│   ├── dependencies.py     # Зависимости (get_db, get_current_user)
│   ├── main.py             # Точка входа
│   ├── models.py           # SQLAlchemy модели
│   ├── schemas.py          # Pydantic схемы
│   └── routers/            
│       ├── books.py        # CRUD книг 
│       ├── borrow.py       # Выдача и возврат 
│       ├── readers.py      # CRUD читателей
│       └── users.py        # Регистрация и логин
│    
├── tests/                  #
│   └── auth.py             # 
│
├── requirements.txt        # List of Python dependencies
└── README.md       

```

## 🚀 Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/AnastasiyaKuzmenko/fastapi-library-api.git  
cd library-api
```
### 2. Создать и активировать виртуальное окружение
```bash
python3 -m venv venv
source ./venv/bin/activate
```
### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Создать файл .env и задать переменные окружения
В файле .env:
```bash
 DATABASE_URL=sqlite:///./library.db
 SECRET_KEY=ваш_секретный_ключ
```
### 5. Применить миграции
```bash
alembic upgrade head
```
### 6. Запустить сервер
```bash
uvicorn app.main:app --reload
```
