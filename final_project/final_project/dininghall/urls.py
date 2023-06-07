from django.urls import path
from . import views

urlpatterns = [
    path('', views.dininghall_index, name="dininghall_index"),
    path('add_menu', views.add_session, name="add_menu"),
    path('edit_menu/<session_id>', views.edit_session, name='edit_menu'),
    path('delete_menu/<session_id>', views.delete_session, name='delete_menu'),
    path('not_dininghall/', views.not_dininghall, name='not_dininghall'),
    path('edit_dropdown/<int:time_id>', views.edit_time, name='edit_dropdown'),
    path('delete_dropdown/<int:time_id>', views.delete_time, name='delete_dropdown'),
]
