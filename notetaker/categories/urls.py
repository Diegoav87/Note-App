from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('<str:username>/', views.UserCategories.as_view(), name='for_user'),
    path('', views.CreateCategory.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteCategory.as_view(), name='delete')
]
