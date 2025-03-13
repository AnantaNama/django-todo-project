from dataclasses import fields
from django import forms

from .models import ToDoItem

class ToDoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ("title", "description")
        
        widgets = {
            "description" : forms.Textarea(attrs={"cols": 30, "rows": 5}),
        }