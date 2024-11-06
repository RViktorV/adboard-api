from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings

from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets

User = get_user_model()  # Получаем кастомную модель пользователя

class RegisterView(generics.CreateAPIView):
    """
    Представление для регистрации новых пользователей.

    Этот класс позволяет создавать новых пользователей. При успешной
    регистрации возвращает данные о пользователе и токены доступа
    (refresh и access) для аутентификации.
    """

    queryset = User.objects.all()  # Запрос для получения всех пользователей
    permission_classes = [permissions.AllowAny]  # Разрешаем доступ для всех пользователей
    serializer_class = RegisterSerializer  # Сериализатор для обработки данных регистрации

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для регистрации нового пользователя.

        Проверяет валидность данных, создает нового пользователя,
        генерирует токены и возвращает их в ответе.

        Args:
            request (Request): HTTP-запрос с данными для регистрации.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Ответ с данными о пользователе и токенами.
        """
        serializer = self.get_serializer(data=request.data)  # Получаем сериализатор с данными запроса
        serializer.is_valid(raise_exception=True)  # Проверяем валидность данных
        user = serializer.save()  # Сохраняем нового пользователя
        refresh = RefreshToken.for_user(user)  # Генерируем токены для нового пользователя
        return Response(
            {
                "user": RegisterSerializer(user, context=self.get_serializer_context()).data,  # Данные пользователя
                "refresh": str(refresh),  # Токен refresh
                "access": str(refresh.access_token),  # Токен access
            }
        )



class ResetPasswordRequestView(APIView):
    """
    Представление для запроса сброса пароля.

    Этот класс обрабатывает запросы на сброс пароля, генерируя
    токен и отправляя ссылку для сброса пароля на указанный
    адрес электронной почты пользователя.
    """

    permission_classes = [AllowAny]  # Разрешает доступ для всех пользователей

    def post(self, request):
        """
        Обрабатывает POST-запрос для сброса пароля.

        Извлекает адрес электронной почты из запроса, проверяет
        наличие пользователя с указанным адресом, генерирует токен
        и отправляет ссылку для сброса пароля на указанный email.

        Args:
            request (Request): Объект запроса, содержащий email пользователя.

        Returns:
            Response: Ответ с сообщением об успешной отправке ссылки
            для сброса пароля или ошибкой, если пользователь не найден.
        """
        email = request.data.get("email")  # Извлекаем email из запроса
        try:
            user = User.objects.get(email=email)  # Находим пользователя по email
            token = default_token_generator.make_token(user)  # Генерируем токен
            uid = urlsafe_base64_encode(force_bytes(user.pk))  # Кодируем ID пользователя

            reset_url = (
                f"{settings.FRONTEND_URL}/reset_password_confirm/{uid}/{token}/"  # Формируем ссылку для сброса пароля
            )

            # Формирование и отправка email
            subject = "Сброс пароля"  # Тема письма
            message = (
                f"Здравствуйте, {user.first_name}!\n\n"
                f"Для сброса пароля перейдите по следующей ссылке: {reset_url}\n\n"
                "Ссылка действительна в течение ограниченного времени.\n\n"
                "Если вы не запрашивали сброс пароля, проигнорируйте это письмо."
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])  # Отправляем email

            return Response(
                {"message": "Ссылка для сброса пароля отправлена на указанный email."}, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response({"error": "Пользователь с таким email не найден."}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordConfirmView(APIView):
    """
    Представление для подтверждения сброса пароля.

    Этот класс обрабатывает запросы на изменение пароля
    после подтверждения токена и UID, полученных в процессе
    сброса пароля.
    """

    permission_classes = [AllowAny]  # Разрешает доступ для всех пользователей

    def post(self, request):
        """
        Обрабатывает POST-запрос для подтверждения сброса пароля.

        Извлекает UID, токен и новый пароль из запроса, проверяет
        их корректность, а затем обновляет пароль пользователя.

        Args:
            request (Request): Объект запроса, содержащий uid, token и new_password.

        Returns:
            Response: Ответ с сообщением об успешном изменении пароля
            или ошибкой, если UID или токен недействительны.
        """
        uid = request.data.get("uid")  # Извлекаем UID из запроса
        token = request.data.get("token")  # Извлекаем токен из запроса
        new_password = request.data.get("new_password")  # Извлекаем новый пароль из запроса

        try:
            user_id = urlsafe_base64_decode(uid).decode()  # Декодируем UID
            user = User.objects.get(pk=user_id)  # Находим пользователя по ID
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Неверный UID."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):  # Проверяем токен
            return Response({"error": "Недействительный или истекший токен."}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:  # Проверяем длину нового пароля
            raise ValidationError("Пароль должен быть не менее 8 символов.")

        user.set_password(new_password)  # Устанавливаем новый пароль
        user.save()  # Сохраняем изменения

        return Response({"message": "Пароль успешно изменён."}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]  # Закрываем доступ авторизацией

# class ResetPasswordRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#
# class ResetPasswordConfirmSerializer(serializers.Serializer):
#     uid = serializers.CharField()
#     token = serializers.CharField()
#     new_password = serializers.CharField(min_length=8)
#
# class ResetPasswordRequestView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         serializer = ResetPasswordRequestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         email = serializer.validated_data['email']
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"message": "Ссылка для сброса пароля отправлена на указанный email."}, status=status.HTTP_200_OK)
#
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         reset_url = f"{settings.FRONTEND_URL}/reset_password_confirm/{uid}/{token}/"
#
#         subject = "Сброс пароля"
#         message = (
#             f"Здравствуйте, {user.first_name}!\n\n"
#             f"Для сброса пароля перейдите по следующей ссылке: {reset_url}\n\n"
#             "Ссылка действительна в течение ограниченного времени.\n\n"
#             "Если вы не запрашивали сброс пароля, проигнорируйте это письмо."
#         )
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
#
#         return Response({"message": "Ссылка для сброса пароля отправлена на указанный email."}, status=status.HTTP_200_OK)
#
# class ResetPasswordConfirmView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         serializer = ResetPasswordConfirmSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         uid = serializer.validated_data['uid']
#         token = serializer.validated_data['token']
#         new_password = serializer.validated_data['new_password']
#
#         try:
#             user_id = urlsafe_base64_decode(uid).decode()
#             user = User.objects.get(pk=user_id)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return Response({"error": "Неверный UID."}, status=status.HTTP_400_BAD_REQUEST)
#
#         if not default_token_generator.check_token(user, token):
#             return Response({"error": "Недействительный или истекший токен."}, status=status.HTTP_400_BAD_REQUEST)
#
#         user.set_password(new_password)
#         user.save()
#
#         return Response({"message": "Пароль успешно изменён."}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    Представление для получения информации о профиле пользователя.
    """

    permission_classes = [IsAuthenticated]  # Доступ только для аутентифицированных пользователей

    def get(self, request):
        """
        Обрабатывает GET-запрос для получения информации о пользователе.

        Args:
            request (Request): Объект запроса.

        Returns:
            Response: Ответ с данными о пользователе.
        """
        user = request.user  # Получаем текущего аутентифицированного пользователя
        user_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "id": user.id,
            "role": user.role,
            "password": user.password,
        }
        return Response(user_data)
