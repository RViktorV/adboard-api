from django.urls import path, include
from .views import AdList, AdDetail, ReviewViewSet, AdCreate
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", ReviewViewSet)

urlpatterns = [
    # path("ads/", AdList.as_view(), name="ad-list"),  # Список и создание объявлений
    path("", AdList.as_view(), name="ad-list"),  # Маршрут для списка объявлений
    path("create/", AdCreate.as_view(), name="ad-create"),  # Маршрут для создания объявления
    path("upd/<int:pk>/", AdDetail.as_view(), name="ad-detail"),  # Получение, обновление и удаление объявления
    path("reviews/", include(router.urls)),  # Подключаем маршруты для отзывов
]
