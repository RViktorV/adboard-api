from rest_framework.pagination import PageNumberPagination


class AdPagination(PageNumberPagination):
    """
    Пагинация для объявлений.
    Ограничение на 4 объекта на странице.
    """

    page_size = 4  # Количество объектов на странице
    page_size_query_param = "page_size"  # Позволяет клиенту задавать размер страницы через параметр запроса
    max_page_size = 100  # Максимально допустимый размер страницы
