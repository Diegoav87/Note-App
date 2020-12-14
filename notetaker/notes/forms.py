from django import forms
from .models import Note
from categories.models import Category


class NoteForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'text', 'category')
        model = Note
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].queryset = Category.objects.filter(user=self.user)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})

