from django import forms
from .models import Category, Color

class CategoryForm(forms.ModelForm):
    class Meta:
        fields = ('name','color')
        model = Category
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        
    