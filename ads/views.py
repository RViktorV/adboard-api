from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Ad, Review
from .permissions import IsAdminOrReadOnly, IsOwner, IsAuthor
from .serializers import AdSerializer, ReviewSerializer
from .pagination import AdPagination


class AdCreate(generics.CreateAPIView):
    """
    Представление для создания нового объявления.

    - POST /ads/create/ - Создать новое объявление.
    """

    queryset = Ad.objects.all()  # Запрос для получения всех объявлений
    serializer_class = AdSerializer  # Сериализатор для преобразования данных
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут создавать объявления

    def perform_create(self, serializer):
        # Устанавливаем поле author на текущего пользователя
        serializer.save(author=self.request.user)


class AdList(generics.ListAPIView):
    """
    Представление для получения списка объявлений.

    - GET /ads/ - Получить список всех объявлений с поддержкой пагинации и поиска.
    """

    queryset = Ad.objects.all()  # Запрос для получения всех объявлений
    serializer_class = AdSerializer  # Сериализатор для преобразования данных
    pagination_class = AdPagination  # Используем пагинацию
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # Подключаем фильтрацию и поиск
    filterset_fields = ["title"]  # Поля, по которым можно фильтровать
    search_fields = ["title", "description"]  # Поля, по которым можно выполнять поиск
    permission_classes = [IsAdminOrReadOnly]  # Анонимные пользователи могут только получать список


class AdDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления конкретного объявления.

    - GET /ads/<id>/ - Получить конкретное объявление по ID.
    - PUT /ads/<id>/ - Обновить конкретное объявление по ID.
    - DELETE /ads/<id>/ - Удалить конкретное объявление по ID.
    """

    queryset = Ad.objects.all()  # Запрос для получения всех объявлений
    serializer_class = AdSerializer  # Сериализатор для преобразования данных
    permission_classes = [
        IsOwner | IsAdminOrReadOnly
    ]  # Пользователь может редактировать/удалять только свои объявления


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с отзывами.
    Поддерживает все CRUD операции.

    - GET /reviews/ - Получить список всех отзывов.
    - POST /reviews/ - Создать новый отзыв.
    - GET /reviews/<id>/ - Получить конкретный отзыв по ID.
    - PUT /reviews/<id>/ - Обновить конкретный отзыв по ID.
    - DELETE /reviews/<id>/ - Удалить конкретный отзыв по ID.
    """

    queryset = Review.objects.all()  # Запрос для получения всех отзывов
    serializer_class = ReviewSerializer  # Сериализатор для преобразования данных
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # Подключаем фильтрацию и поиск
    filterset_fields = ["ad"]  # Поля, по которым можно фильтровать
    search_fields = ["comment"]  # Поля, по которым можно выполнять поиск
    permission_classes = [
        IsOwner | IsAdminOrReadOnly | IsAuthor
    ]  # Пользователь может редактировать/удалять только свои отзывы

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )  # Автоматически устанавливать автора для вошедшего в систему пользователя
