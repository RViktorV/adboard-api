from django.contrib import admin
from .models import Ad, Review

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'ad', 'created_at')
    list_filter = ('author', 'ad', 'created_at')
    search_fields = ('text',)