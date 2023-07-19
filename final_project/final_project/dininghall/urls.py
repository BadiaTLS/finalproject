from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('update_text/<str:value>/', views.update_text, name='update_text'),
    path('update_lrchart/<str:bar>/', views.update_lrchart, name='update_lrchart'),

    path('add_menu', views.add_session, name="add_menu"),
    path('edit_menu_table', views.edit_menu_table, name="edit_menu_table"),
    path('edit_menu_manual/<session_id>', views.edit_session, name='edit_menu_manual'),
    path('edit_dropdown/<int:time_id>', views.edit_time, name='edit_dropdown'),
    
    path('delete_menu/<session_id>', views.delete_session, name='delete_menu'),
    path('delete_dropdown/<int:time_id>', views.delete_time, name='delete_dropdown'),
    
    path('download_report', views.download_report, name='download_report'),

    path('upload_menu_file', views.upload_menu_file, name='upload_menu_file'),
    path('upload_booking_file', views.upload_booking_file, name='upload_booking_file'),
    path('upload_live_booking_file', views.upload_live_booking_file, name='upload_live_booking_file'),

    path('not_dininghall/', views.not_dininghall, name='not_dininghall'),
]
