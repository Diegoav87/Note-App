from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from categories.models import Category
from django.urls import reverse

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='notes', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("notes:user_notes", kwargs={"username": self.user.username})
    
    class Meta:
        ordering = ['title']
    
