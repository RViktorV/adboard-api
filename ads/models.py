from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Получаем модель пользователя

NULLABLE = {"blank": True, "null": True}


class Ad(models.Model):
    """
    Модель объявления.

    Поля:
    - title: Название товара.
    - price: Цена товара (целое число).
    - description: Описание товара.
    - author: Пользователь, который создал объявление.
    - created_at: Время и дата создания объявления.
    """

    title = models.CharField(max_length=255)  # Название товара
    price = models.PositiveIntegerField()  # Цена товара (целое число)
    description = models.TextField()  # Описание товара
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, который создал объявление
    created_at = models.DateTimeField(auto_now_add=True)  # Время и дата создания объявления
    owner = models.ForeignKey(
        User,
        related_name="ads",
        on_delete=models.CASCADE,
        **NULLABLE,
    )  # владелец объявления

    class Meta:
        ordering = ["-created_at"]  # Сортировка по дате создания (чем новее, тем выше)
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        """
        Возвращает строковое представление объекта объявления.

        :return: Название товара.
        """
        return self.title  # Возвращаем название товара при выводе объекта


class Review(models.Model):
    """
    Модель отзыва.

    Поля:
    - text: Текст отзыва.
    - author: Пользователь, который оставил отзыв.
    - ad: Объявление, под которым оставлен отзыв.
    - created_at: Время и дата создания отзыва.
    """

    text = models.TextField()  # Текст отзыва
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, который оставил отзыв
    ad = models.ForeignKey(
        Ad, related_name="reviews", on_delete=models.CASCADE
    )  # Объявление, под которым оставлен отзыв
    created_at = models.DateTimeField(auto_now_add=True)  # Время и дата создания отзыва
    owner = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
        **NULLABLE,
    )  # владелец отзыва

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        """
        Возвращает строковое представление объекта отзыва.

        :return: Строка с информацией об отзыве.
        """
        return f"Review by {self.author} on {self.ad.title}"  # Возвращаем строку с информацией об отзыве
