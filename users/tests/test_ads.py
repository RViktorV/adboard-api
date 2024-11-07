import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ads.models import Ad, Review
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    user = User.objects.create(email="testuser@example.com")
    user.set_password("password123")
    user.save()

    return user


@pytest.fixture
def ad(db, user):
    return Ad.objects.create(
        title="Test Ad",
        price=100,
        description="Test Description",
        author=user,
        owner=user,
    )


@pytest.mark.django_db
def test_create_ad(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("ad-create")
    data = {
        "title": "New Ad",
        "price": 200,
        "description": "New Description",
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Ad.objects.count() == 1
    assert Ad.objects.get().title == "New Ad"


@pytest.mark.django_db
def test_list_ads(api_client, ad, user):
    api_client.force_authenticate(user=user)
    url = reverse("ad-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == ad.title


@pytest.mark.django_db
def test_update_ad(api_client, ad, user):
    api_client.force_authenticate(user=user)
    url = reverse("ad-detail", args=[ad.id])
    data = {
        "title": "Updated Ad",
        "price": 150,
        "description": "Updated Description",
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    ad.refresh_from_db()
    assert ad.title == "Updated Ad"


@pytest.mark.django_db
def test_delete_ad(api_client, ad, user):
    api_client.force_authenticate(user=user)
    url = reverse("ad-detail", args=[ad.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == 0


@pytest.mark.django_db
def test_create_review(api_client, ad, user):
    api_client.force_authenticate(user=user)
    url = reverse("review-list")  # Предполагается, что у вас есть соответствующий маршрут для создания отзыва
    data = {
        "text": "Great product!",
        "ad": ad.id,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1
    assert Review.objects.get().text == "Great product!"


@pytest.mark.django_db
def test_list_reviews(api_client, ad, user):
    api_client.force_authenticate(user=user)
    Review.objects.create(text="Great product!", author=user, ad=ad)
    url = reverse("review-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_update_review(api_client, ad, user):
    review = Review.objects.create(text="Great product!", author=user, ad=ad)
    api_client.force_authenticate(user=user)
    url = reverse("review-detail", args=[review.id])

    # Обновляем данные, включая обязательное поле 'ad'
    data = {
        "text": "Updated review text.",
        "ad": ad.id,  # Добавляем поле 'ad'
    }

    response = api_client.put(url, data)

    # Вывод статуса ответа и данных для диагностики
    print(response.status_code)
    print(response.data)

    assert response.status_code == status.HTTP_200_OK  # Убедитесь, что статус 200
    review.refresh_from_db()
    assert review.text == "Updated review text."


@pytest.mark.django_db
def test_delete_review(api_client, ad, user):
    review = Review.objects.create(text="Great product!", author=user, ad=ad)
    api_client.force_authenticate(user=user)
    url = reverse("review-detail", args=[review.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0
