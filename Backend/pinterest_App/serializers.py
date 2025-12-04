from rest_framework import serializers
from .models import Image, SavedImage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "title", "image_url", "external_id", "source"]

class SavedImageSerializer(serializers.ModelSerializer):
    image = ImageSerializer()  # nested image data

    class Meta:
        model = SavedImage
        fields = ["id", "image", "saved_at"]
