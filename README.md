# AdBoard API

Этот проект представляет собой API-интерфейс бэкенда для бесплатных сайтов, разработанный на Django и Django REST Framework (DRF). API позволяет пользователям создавать и управлять объявлениями и отзывами с поддержкой аутентификации, поиска и пагинации.

## Функции

- **Управление пользователями**: Аутентификация на основе JWT, регистрация пользователей, управление профилями и сброс пароля.
- **Объявления и отзывы**: Операции CRUD для рекламы и обзоров с фильтрацией и нумерацией страниц.
- **Права доступа**: Различные уровни доступа для анонимных пользователей, зарегистрированных пользователей и администраторов.
- **Контейнеризация**: Настройка Docker для простого развертывания, включая поддержку базы данных PostgreSQL.

## Требования

- **Python 3.8+**
- **Django 3.2+**
- **PostgreSQL**
- **Docker & Docker Compose**

## Инструкции по настройке

### 1. Клонирование репозитория

git clone <repository-url>
cd adboard-api

### 2. Настройка переменных окружения

Скопируйте .env.sampleв .env:

cp .env.sample .env
Обновите .env

### 3. Установка зависимостей с помощью Poetry

poetry install

### 4. Упаковка в Docker

docker-compose up --build

### 5. Применение миграций

docker-compose exec web python manage.py migrate

### Основные команды: 
## Авторизация и аутентификация пользователей.

POST: http://127.0.0.1:8000/users/register/ -  регистрация пользователя

POST: http://127.0.0.1:8000/users/login/ -  аутентификация пользователей

POST: http://127.0.0.1:8000/users/reset_password/ -  запрос на смену пароля через электронную почту

POST: http://127.0.0.1:8000/users/reset_password_confirm/ -  подтверждение смены пароля

GET: http://127.0.0.1:8000/users/profile/ -  просмотр профиля пользователя

## Обявления 

POST: http://127.0.0.1:8000/ads/create/ -  создание объявления

GET: http://127.0.0.1:8000/ads/ -  просмотр объявлений

PUT: http://127.0.0.1:8000/ads/upd/2/ -  измение объявления /номер объявления/

DELETE:http://127.0.0.1:8000/ads/upd/2/ -  удаление объявления /номер объявления/

## Отзывы

POST http://127.0.0.1:8000/ads/reviews/ - создание нового отзыва

GET http://127.0.0.1:8000/reviews/1/ - получение конкретного отзыва /номер отзыва/

GET http://127.0.0.1:8000/reviews/ - получение списка отзывов

PUT http://127.0.0.1:8000/reviews/1/ - обновление отзыва /номер отзыва/

DELETE http://127.0.0.1:8000/reviews/1/ - удаление отзыва /номер отзыва/

## фильтрация по названию
GET http://127.0.0.1:8000/ads/?title=Купи%20слона фильтрация по точному названию.

GET http://127.0.0.1:8000/ads/?search=слон фильтрация (поиск) по части названия

### Запкуск тестов
docker-compose exec web pytest -  из под docker

или

pytest - из django
