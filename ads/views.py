from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from .models import Ad, Review
from .serializers import AdSerializer, ReviewSerializer


class AdPagination(PageNumberPagination):
    """
    Пагинация для объявлений.
    Ограничение на 4 объекта на странице.
    """

    page_size = 4  # Количество объектов на странице
    page_size_query_param = "page_size"  # Позволяет клиенту задавать размер страницы через параметр запроса
    max_page_size = 100  # Максимально допустимый размер страницы


class AdCreate(generics.CreateAPIView):
    """
    Представление для создания нового объявления.
    - POST /ads/create/ - Создать новое объявление.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdList(generics.ListAPIView):
    """
    Представление для получения списка объявлений.
    - GET /ads/ - Получить список всех объявлений с поддержкой пагинации и поиска.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ['title']
    search_fields = ['title', 'description']


class AdDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления конкретного объявления.

    - GET /ads/<id>/ - Получить конкретное объявление по ID.
    - PUT /ads/<id>/ - Обновить конкретное объявление по ID.
    - DELETE /ads/<id>/ - Удалить конкретное объявление по ID.
    """

    queryset = Ad.objects.all()  # Запрос для получения всех объявлений
    serializer_class = AdSerializer  # Сериализатор для преобразования данных


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
