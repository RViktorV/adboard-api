import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Получаем модель пользователя
User = get_user_model()

@pytest.fixture
def api_client():
    """
    Фикстура для создания тестового клиента API.
    Возвращает экземпляр APIClient для выполнения HTTP-запросов.
    """
    return APIClient()

@pytest.fixture
def create_user():
    """
    Фикстура для создания пользователя.
    Возвращает функцию, которая позволяет создавать пользователя
    с указанными параметрами (email, password и др.).
    """
    def _create_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return _create_user

@pytest.fixture
def get_tokens_for_user(create_user):
    """
    Фикстура для получения JWT токенов для аутентификации пользователя.
    Возвращает функцию, которая создает пользователя и генерирует
    для него access и refresh токены.
    """
    def _get_tokens(email, password):
        user = create_user(email=email, password=password)  # Создаем пользователя
        refresh = RefreshToken.for_user(user)  # Генерируем токен для пользователя
        return str(refresh.access_token), str(refresh)  # Возвращаем access и refresh токены

    return _get_tokens

@pytest.mark.django_db
def test_register_user(api_client):
    """
    Тестирует процесс регистрации нового пользователя.
    """
    url = reverse('users:register')  # URL для регистрации
    data = {
        'email': 'testuser@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }

    response = api_client.post(url, data)  # Выполняем POST-запрос на регистрацию

    # Проверяем, что запрос завершился успешно
    assert response.status_code == status.HTTP_200_OK
    assert 'user' in response.data
    assert 'access' in response.data
    assert 'refresh' in response.data

# # @pytest.mark.django_db
# # def test_reset_password_request(api_client, create_user):
# #     """
# #     Тестирует запрос на сброс пароля и подтверждение сброса пароля.
# #     """
# #     # Сначала создаем пользователя
# #     user = create_user(email='testuser@example.com', password='password123')
# #
# #     # Первый шаг: отправка запроса на сброс пароля
# #     url_reset_request = reverse('users:reset_password')  # URL для запроса на сброс пароля
# #     data_reset_request = {'email': 'testuser@example.com'}
# #
# #     response_reset_request = api_client.post(url_reset_request, data_reset_request)  # Выполняем запрос на сброс
# #
# #     # Проверяем, что запрос на сброс пароля завершился успешно
# #     assert response_reset_request.status_code == status.HTTP_200_OK
# #     assert "Ссылка для сброса пароля отправлена" in response_reset_request.data['message']
# #
# #     # Дополнительно можно проверить, что письмо отправлено (если есть Celery/фейковая почта)
# #
# #     # Второй шаг: подтверждение сброса пароля (здесь предполагается, что ты знаешь токен сброса)
# #     reset_token = 'example_token_from_email'  # Токен, который должен прийти на почту пользователя
# #
# #     url_reset_confirm = reverse('users:reset_password_confirm')  # URL для подтверждения сброса пароля
# #     data_reset_confirm = {
# #         'token': reset_token,  # Токен для сброса пароля
# #         'email': 'testuser@example.com',
# #         'new_password': 'new_password123'
# #     }
# #
# #     response_reset_confirm = api_client.post(url_reset_confirm, data_reset_confirm)  # Выполняем запрос
# #
# #     # Проверяем, что запрос на подтверждение сброса пароля завершился успешно
# #     assert response_reset_confirm.status_code == status.HTTP_200_OK
# #     assert "Пароль успешно изменен" in response_reset_confirm.data['message']
# #
# #     # Проверяем, что пользователь может войти с новым паролем
# #     login_url = reverse('users:login')
# #     login_data = {
# #         'email': 'testuser@example.com',
# #         'password': 'new_password123'
# #     }
# #
# #     login_response = api_client.post(login_url, login_data)
# #     assert login_response.status_code == status.HTTP_200_OK
# #     assert 'access' in login_response.data
# #     assert 'refresh' in login_response.data
#
# @pytest.mark.django_db
# def test_user_profile(api_client, get_tokens_for_user):
#     """
#     Тестирует получение профиля пользователя.
#     """
#     access_token, _ = get_tokens_for_user(email='testuser@example.com', password='password123')
#
#     url = reverse('users:profile')  # Правильный путь для профиля
#     api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
#
#     response = api_client.get(url)  # Выполняем GET-запрос
#
#     # Проверяем, что запрос завершился успешно и данные профиля корректны
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['email'] == 'testuser@example.com'
#     assert 'first_name' in response.data
#     assert 'last_name' in response.data
#
# @pytest.mark.django_db
# def test_invalid_password_reset_request(api_client):
#     """
#     Тестирует запрос на сброс пароля с несуществующим email.
#     """
#     url = reverse('users:reset_password')  # Правильный путь для сброса пароля
#     data = {'email': 'nonexistent@example.com'}
#
#     response = api_client.post(url, data)  # Выполняем POST-запрос
#
#     # Проверяем, что запрос завершился с ошибкой 404
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#     assert "Пользователь с таким email не найден" in response.data['error']
