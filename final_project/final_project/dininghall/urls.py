from django.urls import path
from . import views

urlpatterns = [
    path('', views.dininghall_home_page, name="dininghall_home_page"),
    path('edit_menu_table', views.edit_menu_table, name="edit_menu_table"),
    path('add_menu', views.add_session, name="add_menu"),
    path('edit_menu_manual/<session_id>', views.edit_session, name='edit_menu_manual'),
    path('delete_menu/<session_id>', views.delete_session, name='delete_menu'),
    path('not_dininghall/', views.not_dininghall, name='not_dininghall'),
    path('edit_dropdown/<int:time_id>', views.edit_time, name='edit_dropdown'),
    path('delete_dropdown/<int:time_id>', views.delete_time, name='delete_dropdown'),
    path('upload_menu_file', views.upload_menu_file, name='upload_menu_file'),
    path('download_report', views.download_report, name='download_report'),
]
