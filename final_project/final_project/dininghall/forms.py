from django import forms
from django.forms import ModelForm
from .models import table_session, table_time

class SessionForm(ModelForm):
    class Meta:
        model = table_session
        fields = "date", "name", "menu"
        widgets = {
            "date": forms.DateInput(attrs={"class":"form-control", "type":"date"}),
            "name": forms.Select(attrs={"class":"form-control"}),
            "menu": forms.TextInput(attrs={"class":"form-control"}),
        }

class TimeForm(ModelForm):
    class Meta:
        model = table_time
        fields = "seat_limit",
        widgets = {
            "seat_limit": forms.NumberInput(attrs={"class":"form-control"})
        }