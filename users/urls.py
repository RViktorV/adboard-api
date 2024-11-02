from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView
from users.apps import UsersConfig
from . import views


app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("reset_password/", views.ResetPasswordRequestView.as_view(), name="reset_password"),
    path("reset_password_confirm/',", views.ResetPasswordConfirmView.as_view(), name="reset_password_confirm"),
]
