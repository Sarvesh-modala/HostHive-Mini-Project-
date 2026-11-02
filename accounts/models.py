from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extended user model with role-based permissions"""
    USER_TYPES = (
        ('host', 'Host'),
        ('client', 'Client'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client')
    phone = models.CharField(max_length=15, blank=True)
    
    def is_host(self):
        return self.user_type == 'host'
    
    def is_client(self):
        return self.user_type == 'client'