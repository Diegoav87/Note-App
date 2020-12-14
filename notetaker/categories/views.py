from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from .models import Category
from django.http import Http404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
User = get_user_model()
from . import forms

from braces.views import SelectRelatedMixin


# Create your views here.
class CreateCategory(generic.CreateView, SelectRelatedMixin, LoginRequiredMixin):
    model = Category
    form_class = forms.CategoryForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class UserCategories(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'categories/user_category_list.html'

    def get_queryset(self):
        self.category_user = User.objects.get(id=self.request.user.id)
        return self.category_user.user_categories.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_user"] = self.category_user 
        return context

class DeleteCategory(generic.DeleteView, LoginRequiredMixin):
    model = Category
    
    def get_success_url(self):
        return reverse_lazy('categories:for_user', kwargs={'username': self.request.user.username})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Category Deleted")
        return super().delete(*args, **kwargs)
    

    
    
