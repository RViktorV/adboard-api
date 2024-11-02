from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Административный интерфейс для модели Users.

    Этот класс настраивает отображение и управление пользователями
    в административной панели Django. Он наследует от UserAdmin
    и позволяет управлять полями, связанными с пользователем.
    """

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Поля для ввода email и пароля
        ('Personal info', {'fields': ('phone', 'avatar', 'first_name', 'last_name')}),  # Личная информация пользователя
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # Права доступа
        ('Important dates', {'fields': ('last_login', 'date_joined')}),  # Важные даты
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # Широкий класс для отображения
            'fields': ('email', 'phone', 'password1', 'password2'),  # Поля для добавления нового пользователя
        }),
    )

    list_display = ('email', 'phone', 'is_staff')  # Поля, отображаемые в списке пользователей
    search_fields = ('email', 'phone')  # Поля, по которым можно осуществлять поиск
    ordering = ('email',)  # Поле, по которому будет происходить сортировка