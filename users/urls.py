from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserViewSet, UserProfileView
from users.apps import UsersConfig
from . import views
from rest_framework.routers import DefaultRouter


app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet)  # CRUD для пользователей

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("reset_password/", views.ResetPasswordRequestView.as_view(), name="reset_password"),
    path("reset_password_confirm/", views.ResetPasswordConfirmView.as_view(), name="reset_password_confirm"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
]
