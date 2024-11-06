from .settings import *  # Импортируем все основные настройки

# Настройки базы данных для тестов
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}