from django.db import models
from app_auth.models import User


class Note(models.Model):
    """Note model for storing user notes"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return f"{self.title} - {self.user.email}"
