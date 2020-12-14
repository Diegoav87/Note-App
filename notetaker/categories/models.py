from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_categories')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("categories:for_user", kwargs={'username': self.user.username})
    

    class Meta:
        ordering = ['name']
    