# API YaMDb

REST API для платформы отзывов на произведения (книги, фильмы, музыка).
Пользователи могут оставлять отзывы, ставить оценки и комментировать чужие отзывы.

Реализовано:
- кастомная модель пользователей
- система ролей (user, moderator, admin)
- JWT-аутентификация
- динамический рейтинг произведений на основе отзывов

---

## Технологии

- Python 3.12
- Django 5.1
- Django REST Framework (DRF)
- SimpleJWT
- django-filter
- SQLite

---

## Установка и запуск

Клонировать репозиторий:

```bash
git clone git@github.com:KamilKhairullin2003/api_yamdb.git
cd api_yamdb
```

Создать и активировать виртуальное окружение:

Windows:
```bash
python -m venv env
source env/Scripts/activate
```

Linux/macOS:

```bash
python3 -m venv env
source env/bin/activate
```

Установить зависимости:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Применить миграции:

```bash
python manage.py migrate
```

Запустить сервер:

```bash
python manage.py runserver
```
---

## Аутентификация (JWT)

1. Регистрация
POST /api/v1/auth/signup/

{
  "email": "user@example.com",
  "username": "username"
}

2. Получение токена
POST /api/v1/auth/token/

{
  "username": "username",
  "confirmation_code": "code"
}

Ответ:
{
  "token": "your_jwt_token"
}

3. Использование токена

Authorization: Bearer <token>

---

## Примеры запросов

Получение списка произведений:
GET /api/v1/titles/

Добавление отзыва:
POST /api/v1/titles/{title_id}/reviews/

{
  "text": "Шедевр мирового кинематографа!",
  "score": 10
}

Получение комментариев:
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/

---

## Автор

Камиль Хайруллин
Python Backend Developer

Telegram: @kamildja
Email: crewt1e@yandex.ru
