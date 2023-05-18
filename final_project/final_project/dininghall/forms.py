from django import forms
from django.forms import ModelForm
from .models import table_menu

class MenuForm(ModelForm):
    class Meta:
        model = table_menu
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"class":"form-control", "type":"date"}),
            "session": forms.Select(attrs={"class":"form-control"}),
            "menu": forms.TextInput(attrs={"class":"form-control"}),
        }