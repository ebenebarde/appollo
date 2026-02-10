from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    email = models.EmailField(unique=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.username}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username
