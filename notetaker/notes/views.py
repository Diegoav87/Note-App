from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from . import models
from . import forms
from categories.models import Category

from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class UserNotes(LoginRequiredMixin, generic.ListView):
    model = models.Note
    template_name = 'notes/user_note_list.html'

    def get_queryset(self):
        self.note_user = User.objects.get(id=self.request.user.id)
        return self.note_user.notes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["note_user"] = self.note_user 
        return context

class CreateNote(generic.CreateView, LoginRequiredMixin):
    form_class = forms.NoteForm
    model = models.Note

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

class DeleteNote(generic.DeleteView, LoginRequiredMixin, SelectRelatedMixin):
    select_related = ('user', 'category')
    model = models.Note
    
    def get_success_url(self):
        return reverse_lazy('notes:user_notes', kwargs={'username': self.request.user.username})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Note Deleted")
        return super().delete(*args, **kwargs)

class UserCategoryNotes(LoginRequiredMixin, generic.ListView):
    model = models.Note
    template_name = 'notes/user_category_notes.html'

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs.get('pk'))
        queryset = super().get_queryset()
        return queryset.filter(user__id=self.request.user.id, category=category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_category_notes"] = self.get_queryset()
        return context

class UpdateNote(generic.UpdateView, LoginRequiredMixin):
    model = models.Note
    form_class = forms.NoteForm

    def get_success_url(self):
        return reverse_lazy('notes:user_notes', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs