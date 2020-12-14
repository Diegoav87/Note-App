from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('<str:username>/', views.UserNotes.as_view(), name='user_notes'),
    path('', views.CreateNote.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteNote.as_view(), name='delete'),
    path('<str:username>/<int:pk>/', views.UserCategoryNotes.as_view(), name='user_category_notes'),
    path('edit/note/<int:pk>/', views.UpdateNote.as_view(), name='update')
]
