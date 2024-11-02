from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации новых пользователей.

    Этот сериализатор обрабатывает данные, необходимые для создания
    нового пользователя, включая валидацию и шифрование пароля.
    """

    password = serializers.CharField(write_only=True)  # Поле для пароля, доступное только для записи

    class Meta:
        model = User  # Модель, с которой будет работать сериализатор
        fields = ('email', 'first_name', 'last_name', 'password', 'phone', 'role', 'avatar')  # Поля, которые будут сериализованы

    def create(self, validated_data):
        """
        Создает нового пользователя с валидированными данными.

        Извлекает данные из валидированного словаря, создает экземпляр
        пользователя и шифрует его пароль перед сохранением в базе данных.

        Args:
            validated_data (dict): Словарь с валидированными данными для создания пользователя.

        Returns:
            User: Созданный объект пользователя.
        """
        user = User(
            email=validated_data['email'],  # Устанавливаем email
            first_name=validated_data['first_name'],  # Устанавливаем имя
            last_name=validated_data['last_name'],  # Устанавливаем фамилию
            phone=validated_data.get('phone', ''),  # Устанавливаем телефон, если он есть
            role=validated_data.get('role', 'user'),  # Устанавливаем роль, по умолчанию 'user'
        )
        user.set_password(validated_data['password'])  # Шифруем пароль
        user.save()  # Сохраняем пользователя в базе данных
        return user  # Возвращаем созданного пользователя
