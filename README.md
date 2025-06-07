# 📚 Library API

RESTful API для управления библиотечным каталогом с системой выдачи и возврата книг. Разработан с использованием FastAPI, SQLAlchemy, JWT-аутентификации и Alembic для миграций.


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
├── tests/                  # Pytest тесты
│   ├── conftest.py          
│   ├── test_books.py        
│   ├── test_borrow.py       
│   ├── test_readers.py      
│   └── test_users.py        
│
├── requirements.txt        # Зависимости
│
├── run_test.sh             # Запускает pytest тесты и flake8    
│
├── .flake8                 # Настройки flake8     
│    
└── README.md       

```

## 🚀 Установка и запуск

#### 1. Клонировать репозиторий
```bash
git clone https://github.com/AnastasiyaKuzmenko/fastapi-library-api.git  
cd fastapi-library-api
```
#### 2. Создать и активировать виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```
#### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

#### 4. Создать файл .env и задать переменные окружения
В файле .env:
```bash
 DATABASE_URL=sqlite:///./library.db
 SECRET_KEY=ваш_секретный_ключ
```
#### 5. Применить миграции
```bash
alembic upgrade head
```
#### 6. Запустить сервер
```bash
uvicorn app.main:app --reload
```

## 🧪 Тестирование
#### Запуск только pytest тестов
```bash
pytest tests/
```
#### Запуск pytest тестов и проверки синтаксиса с помощью flake8
```bash
chmod +x run_test.sh
./run_test.sh
```

## 🔐 Аутентификация
- Регистрация: POST `/auth/register` — создание пользователя с email и паролем.
- Вход: POST `/auth/login` — возврат JWT-токена.
- Защищённые эндпоинты:
    - Все CRUD-операции над книгами, читателями, а также выдача/возврат книг защищены JWT.
    - Исключения: `/users/register`, `/users/login`, `/books/`, `/books/{book_id}` — публичны.
    Эндпоинты получения книг (`GET /books/` и  `GET /books/{id}`) оставлены открытыми, так как доступ к каталогу может быть полезен для читателей тоже.

- Используются библиотеки:
    - `python-jose` для работы с JWT.
    - `passlib[bcrypt]` для хеширования паролей.
- Как работает:
    - При регистрации пользователь отправляет email и пароль. Пароль хешируется и сохраняется.
    - При логине генерируется JWT токен, который содержит `sub = user.email` и срок действия.
    - Все защищённые маршруты используют Depends(`get_current_user`)

## 🧱 Принятые решения по структуре БД
- Пользователи (User) — для аутентификации библиотекарей. Содержит email и хешированный пароль.
- Книги (Book) — основная информация о книгах, включая уникальный ISBN и количество доступных экземпляров.
- Читатели (Reader) — управляются только библиотекарями, содержат имя и уникальный email.
- Выдачи (BorrowedBook) — отдельная таблица для фиксации фактов выдачи, содержит book_id, reader_id, дату выдачи и дату возврата (return_date).

## 🧠 Реализация бизнес-логики
#### 1. Выдача книги (`/borrow/checkout`):

- Проверка доступности экземпляров: copies_available > 0
- Проверка лимита у читателя: не более 3 книг
- При успешной выдаче:
    - уменьшается copies_available на 1
    - создаётся запись в BorrowedBooks с `return_date = NULL`

#### 2. Возврат книги (`/borrow/return`):
- Проверка, что запись о выдаче существует и не возвращена
- Увеличивается copies_available на 1
- Устанавливается `return_date = текущая дата`

#### 3. Запрет на повторную выдачу уже выданной книги, и возврат уже возвращённой — обрабатывается бизнес-логикой через проверки 
`return_date IS NULL.`


## ❗ Сложности и как они были решены
- JWT токен не подхватывался:
Добавлена функция зависимости get_current_user, обрабатывающая OAuth2PasswordBearer.

- Проблема с возвратом уже возвращённой книги:
Добавлена проверка return_date IS NULL при возврате.

- Ограничение на 3 книги у читателя:
Реализовано через SQL-запрос count() по BorrowedBooks WHERE reader_id=? AND return_date IS NULL.

- Добавление поля через миграцию:
Использован alembic revision --autogenerate для поля description в таблице Book.