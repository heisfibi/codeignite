from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    username_updated_at = models.DateTimeField(auto_now_add=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
