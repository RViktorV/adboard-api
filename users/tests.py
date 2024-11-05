from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User

class UserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="testuser@example.com", password="password"
        )
        self.user.set_password("password")  # Убедитесь, что пароль хеширован
        self.user.save()

    def test_get_users_list(self):
        """
        Тестовое получение списка пользователей (требуется аутентификация).
        """
        self.client.force_authenticate(user=self.user)  # Аутентифицированный запрос
        url = reverse('users:users-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        """
        Тестовая регистрация пользователя.
        """
        url = reverse('users:register')
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "telegram_id": "654321"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Users.objects.filter(email="newuser@example.com").exists())

    def test_login_user(self):
        """
        Проверьте вход пользователя, чтобы получить токен JWT.
        """
        url = reverse('users:login')
        data = {
            "email": "testuser@example.com",
            "password": "password",
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """
        Test refreshing JWT token.
        """
        login_url = reverse('users:login')  # Use the correct 'login' URL
        login_data = {
            "email": "testuser@example.com",
            "password": "password"
        }
        login_response = self.client.post(login_url, login_data, format='json')
        print(login_response.data)

        # Проверьте, был ли вход успешным и токены были возвращены
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', login_response.data)
        refresh_token = login_response.data['refresh']

        refresh_url = reverse('users:token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_user_detail(self):
        """
        Тестирование получения конкретных сведений о пользователе.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('users:users-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user(self):
        """
        Тестовое обновление данных пользователя.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('users:users-detail', kwargs={'pk': self.user.id})
        data = {
            'city': 'New City'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], 'New City')

    def test_delete_user(self):
        """
        Тестовое удаление пользователя.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('users:users-detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Users.objects.filter(id=self.user.id).exists())