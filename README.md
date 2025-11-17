# User Management API с ролями

FastAPI приложение для управления пользователями с системой ролей (админ/пользователь).

## Структура проекта

```
.
├── src/
│   ├── auth.py              
│   ├── crud.py              
│   ├── database.py          
│   ├── main.py              
│   ├── models.py            
│   ├── schemas.py           
│   ├── seed.py              
│   └── routers/
│       ├── auth.py          
│       └── products.py      
├── docker-compose.yml       
├── Dockerfile               
├── requirements.txt         
└── README.md               
```

## Установка и запуск

### Docker запуск

```bash
docker-compose up --build
```

## Тестовые данные

При запуске приложения автоматически создаются тестовые пользователи:

### Админ
- Email: admin@example.com
- Password: admin123
- Роль: admin

### Пользователь
- Email: user@example.com
- Password: user123
- Роль: user

## API Эндпоинты

### Аутентификация

#### Регистрация
```
POST /auth/register
```
**Тело запроса:**
```json
{
  "first_name": "Иван",
  "last_name": "Иванов",
  "email": "ivan@example.com",
  "password": "password123",
  "password_confirm": "password123"
}
```

#### Вход в систему
```
POST /auth/login
```
**Тело запроса:**
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```
**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Получение информации о себе
```
GET /auth/me
```
**Заголовки:** `Authorization: Bearer <token>`

#### Обновление профиля
```
PUT /auth/me
```
**Заголовки:** `Authorization: Bearer <token>`
**Тело запроса:**
```json
{
  "first_name": "Новое имя",
  "last_name": "Новая фамилия",
  "email": "newemail@example.com"
}
```

#### Деактивация аккаунта
```
DELETE /auth/me
```
**Заголовки:** `Authorization: Bearer <token>`

#### Выход из системы
```
POST /auth/logout
```
**Заголовки:** `Authorization: Bearer <token>`

### Админские функции

#### Получить всех пользователей
```
GET /admin/users
```
**Заголовки:** `Authorization: Bearer <token>` (только для админов)

#### Удалить пользователя
```
DELETE /admin/users/{user_id}
```
**Заголовки:** `Authorization: Bearer <token>` (только для админов)

### Товары

#### Получить все товары
```
GET /products
```
**Заголовки:** `Authorization: Bearer <token>`
**Параметры:**
- `category` (опционально): фильтр по категории

**Поведение:**
- Админ видит все товары
- Пользователь видит только свои товары

#### Получить товар по ID
```
GET /products/{product_id}
```
**Заголовки:** `Authorization: Bearer <token>`

#### Создать товар
```
POST /products
```
**Заголовки:** `Authorization: Bearer <token>`
**Тело запроса:**
```json
{
  "name": "Ноутбук Lenovo",
  "description": "Бизнес-ноутбук",
  "price": 85000,
  "category": "Электроника"
}
```

#### Обновить товар
```
PUT /products/{product_id}
```
**Заголовки:** `Authorization: Bearer <token>`
**Тело запроса:**
```json
{
  "name": "Обновленный ноутбук",
  "description": "Обновленное описание",
  "price": 90000,
  "category": "Электроника"
}
```

#### Удалить товар
```
DELETE /products/{product_id}
```
**Заголовки:** `Authorization: Bearer <token>`

## Ролевая модель

### Админ (admin)
- Полный доступ ко всем пользователям
- Полный доступ ко всем товарам
- Может создавать/изменять/удалять любые товары

### Пользователь (user)
- Доступ только к своему профилю
- Может создавать/изменять/удалять только свои товары
- Видит только свои товары в списке

## Документация API

Полная интерактивная документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs

## Технологии

- **FastAPI**: Веб-фреймворк
- **SQLAlchemy**: ORM для работы с БД
- **PostgreSQL**: База данных
- **Pydantic**: Валидация данных
- **PassLib**: Хеширование паролей
- **PyJWT**: JWT токены
- **Docker**: Контейнеризация

## Тестирование

### Регистрация и вход
```bash
# Регистрация
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Тест",
    "last_name": "Пользователь",
    "email": "test@example.com",
    "password": "test123",
    "password_confirm": "test123"
  }'

# Вход
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

### Работа с товарами
```bash
# Получить токен (замените на реальный)
TOKEN="your-jwt-token-here"

# Создать товар
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тестовый товар",
    "description": "Описание товара",
    "price": 1000,
    "category": "Тест"
  }'

# Получить товары
curl -X GET "http://localhost:8000/products" \
  -H "Authorization: Bearer $TOKEN"
