# AutoRia Clone — Car Marketplace API

Масштабована платформа для купівлі та продажу автомобілів побудована на Django REST Framework.

## Технічний стек

- **Backend**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL 16
- **Cache / Queue broker**: Redis 7
- **Task Queue**: Celery 5
- **Containerization**: Docker + Docker Compose
- **Auth**: JWT (djangorestframework-simplejwt)

## Ролі користувачів

| Роль | Опис |
|------|------|
| Buyer | Перегляд оголошень |
| Seller | Створення оголошень (Basic: 1, Premium: необмежено) |
| Manager | Модерація оголошень |
| Admin | Повний доступ |

## Типи акаунтів

| Тип | Ліміт оголошень | Статистика |
|-----|-----------------|------------|
| Basic | 1 активне | Ні |
| Premium | Необмежено | Так |

## Запуск локально

### Вимоги
- Docker Desktop
- Git

### Кроки

**1. Клонуй репозиторій**
```bash
git clone https://github.com/your-username/autoria.git
cd autoria
```

**2. Створи `.env` файл**
```bash
cp .env.example .env
```

**3. Запусти контейнери**
```bash
docker compose up --build
```

**4. Застосуй міграції**
```bash
docker compose exec web python manage.py migrate
```

**5. Створи суперкористувача**
```bash
docker compose exec web python manage.py createsuperuser
```

**6. Відкрий браузер**
- API: http://localhost:8000
- Admin: http://localhost:8000/admin

## API Endpoints

### Auth
| Метод | URL | Опис | Доступ |
|-------|-----|------|--------|
| POST | `/auth/register/` | Реєстрація | Публічний |
| POST | `/auth/login/` | Логін (JWT) | Публічний |
| POST | `/auth/token/refresh/` | Оновити токен | Публічний |
| GET | `/auth/me/` | Мій профіль | Авторизований |

### Cars
| Метод | URL | Опис | Доступ |
|-------|-----|------|--------|
| GET | `/cars/` | Список оголошень | Публічний |
| POST | `/cars/` | Створити оголошення | Seller/Admin |
| GET | `/cars/<id>/` | Деталі оголошення | Публічний |
| PUT | `/cars/<id>/` | Редагувати | Власник/Manager/Admin |
| DELETE | `/cars/<id>/` | Видалити | Власник/Manager/Admin |
| GET | `/cars/makes/` | Список марок | Публічний |
| GET | `/cars/makes/<id>/models/` | Моделі марки | Публічний |

### Pricing
| Метод | URL | Опис | Доступ |
|-------|-----|------|--------|
| GET | `/pricing/rates/` | Поточні курси валют | Публічний |
| GET | `/pricing/rates/refresh/` | Оновити курси | Admin |

### Stats
| Метод | URL | Опис | Доступ |
|-------|-----|------|--------|
| GET | `/stats/<car_id>/` | Статистика оголошення | Premium власник |
| POST | `/stats/<car_id>/view/` | Записати перегляд | Публічний |

### Moderation
| Метод | URL | Опис | Доступ |
|-------|-----|------|--------|
| GET | `/moderation/pending/` | Очікують модерації | Manager/Admin |
| POST | `/moderation/cars/<id>/moderate/` | Модерувати | Manager/Admin |
| GET | `/moderation/cars/<id>/logs/` | Історія модерації | Manager/Admin |
## Urls documentation
http://localhost:8000/api/docs/
## Запуск тестів
```bash
docker compose exec web python manage.py test apps.users apps.cars apps.pricing apps.moderation
```

## Структура проєкту
```
autoria/
├── apps/
│   ├── users/          # Користувачі, ролі, JWT
│   ├── cars/           # Оголошення, марки, моделі
│   ├── pricing/        # Курси валют, конвертація
│   ├── moderation/     # Модерація тексту
│   ├── stats/          # Статистика переглядів
│   └── notifications/  # Email сповіщення
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── celery.py
│   └── urls.py
├── .env
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

## Змінні середовища

Створи `.env` файл на основі цього шаблону:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=autoria
POSTGRES_USER=autoria_user
POSTGRES_PASSWORD=autoria_pass
DATABASE_URL=postgres://autoria_user:autoria_pass@db:5432/autoria

REDIS_URL=redis://redis:6379/0
```

## Celery задачі

| Задача | Розклад | Опис |
|--------|---------|------|
| `update_exchange_rates` | Щодня о 9:00 | Оновлює курси з ПриватБанку |
| `send_moderation_notification` | При події | Email менеджеру |
| `send_listing_flagged_notification` | При події | Email продавцю |