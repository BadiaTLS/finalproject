from django.urls import path
from . import views

urlpatterns = [
    path('', views.dininghall_index, name="dininghall_index"),
    path('add_menu', views.add_session, name="add_menu"),
    path('edit_menu/<menu_id>', views.edit_session, name='edit_menu'),
    path('delete_menu/<menu_id>', views.delete_session, name='delete_menu'),
    path('not_dininghall/', views.not_dininghall, name='not_dininghall'),
]
