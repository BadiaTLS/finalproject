from django.shortcuts import redirect
from .models import table_menu

def get_all_menu_objects():
    return table_menu.objects.all()

def save_menu(form):
    form.save()

def get_menu_by_id(menu_id):
    return table_menu.objects.get(pk=menu_id)

def update_menu(form):
    form.save()
    
def delete_menu_object(menu):
    menu.delete()
