from django.urls import path
from . import views

urlpatterns = [
    path('', views.dininghall_index, name="dininghall_index"),
    path('add_menu', views.add_menu, name="add_menu"),
    path('edit_menu/<menu_id>', views.edit_menu, name='edit_menu'),
    path('delete_menu/<menu_id>', views.delete_menu, name='delete_menu'),
]