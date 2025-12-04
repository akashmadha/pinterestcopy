from django.contrib import admin
from .models import Image, SavedImage

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "source", "external_id", "image_url", "created_at")
    search_fields = ("title", "external_id", "source")

@admin.register(SavedImage)
class SavedImageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "image", "saved_at")
    list_filter = ("saved_at", "user")
    search_fields = ("user__username", "image__title")
