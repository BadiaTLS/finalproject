from django import forms
from django.forms import ModelForm
from .models import table_students_information
from final_project.dininghall.models import table_time, table_session

class MenuForm(ModelForm):
    class Meta:
        model = table_students_information
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"class":"form-control", "type":"date"}),
            "session": forms.Select(attrs={"class":"form-control"}),
            "menu": forms.TextInput(attrs={"class":"form-control"}),
        }

class ConfirmForm(forms.Form):
    time_object = forms.TimeField()
    session_object = forms.CharField()
    current_date = forms.DateField()
    session = forms.CharField()
    # session_object = forms.ModelChoiceField(queryset=table_session.objects.all())