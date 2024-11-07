from rest_framework import serializers
from .models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = (
            "title",
            "price",
            "description",
            "created_at",
            "owner",
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "ad",
            "created_at",
        )
