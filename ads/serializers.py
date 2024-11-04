from rest_framework import serializers
from .models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "author",
            "ad",
            "created_at",
        )
