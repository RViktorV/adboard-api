from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):

    username = None  # Убираем поле username

    ROLE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
    ]
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Электронная почта")

    phone = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
        **NULLABLE,
    )

    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default="user")

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    avatar = models.ImageField(
        upload_to="users/avatars/",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Возвращает строковое представление пользователя — его email.
        """
        return self.email
