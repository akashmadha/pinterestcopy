from django.db import models

# pinterest_App/models.py

class Post(models.Model):
    pixabay_id = models.CharField(max_length=255, unique=True)
    image_url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Image(models.Model):
    # If images are only external URLs, image_url is enough.
    # If you later want to upload files, replace URLField with ImageField.
    external_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional id from external API (e.g. unsplash id)."
    )
    title = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=2000 ,blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, help_text="Optional source name (Unsplash/Custom)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return self.title or self.image_url

class SavedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_images")
    image = models.ForeignKey(Image, on_delete=models.CASCADE,blank=True, null=True, related_name="saved_by")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "image")
        ordering = ["-saved_at"]

    def __str__(self):
        return f"{self.user} saved {self.image.id}"
