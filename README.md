# Support Chat Bot (FastAPI)

## Установка
- Установите Python 3.13+
- Создайте виртуальное окружение и установите зависимости:  
  `python -m venv .venv`  
  `.venv\Scripts\activate`  
  `pip install -r requirements.txt`

## Миграции
- Инициализация базы данных:  
  `alembic upgrade head`
- Переменная `DATABASE_URL` по умолчанию: `sqlite+aiosqlite:///./app.db`  
  В `alembic.ini` используется `sqlite:///./app.db`

## Запуск
- `uvicorn app.main:app --reload`
- Открыть `http://localhost:8000/docs`

## Эндпоинты
- `POST /auth/register` тело: `{"username": "...", "password": "..."}`  
  ответ: пользователь
- `POST /auth/login` тело: `{"username": "...", "password": "..."}`  
  ответ: `{"access_token":"...", "token_type":"bearer"}`
- `POST /chat/session` заголовок `Authorization: Bearer <token>`  
  ответ: `{"session_id": ...}`
- `POST /chat/message` заголовок `Authorization`  
  тело: `{"session_id": ..., "text": "..."}`  
  ответ: сообщение бота
- `GET /chat/history/{session_id}` заголовок `Authorization`  
  ответ: история сообщений
- `WebSocket /ws/chat?token=<jwt>&session_id=<id>` обмен JSON

## Валидация и ошибки
- Pydantic проверяет обязательные поля, длину строк и пустые значения
- Ошибки 401 при невалидном токене, 404 при чужой или отсутствующей сессии, 400 при конфликте регистрации

## Логика бота
- Ключевые слова: привет, помощь, поддержка, оплата  
- Ответ по умолчанию при отсутствии совпадений

## CORS
- Разрешены: `http://localhost`, `http://localhost:8080`  
  `allow_credentials=True`, `allow_methods=["*"]`, `allow_headers=["*"]`

## Тестирование
- `pytest -q`  
- Тесты используют временную SQLite-базу и фикстуры

## Логирование
- Базовая конфигурация `logging` уровня INFO

## Защита и документация
- Swagger UI доступен по `http://localhost:8000/docs`
- Пароли хэшируются `bcrypt`, аутентификация через JWT
