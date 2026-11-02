from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Category(models.Model):
    """Category model for event classification with background videos"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'host'})
    background_video = models.FileField(upload_to='videos/', blank=True, null=True)
    image = models.ImageField(upload_to='images/categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'pk': self.pk})