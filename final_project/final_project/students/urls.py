from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_index, name="student_index"),
    path('dining_hall/', views.students_home_view_dininghall, name="dining_hall"),
    path('library', views.students_home_view_library, name="library"),
    path('laboratorium', views.students_home_view_laboratorium, name="laboratorium"),

    path('dining_hall/confirm', views.confirm, name="confirm_dininghall_booking"),
    path('dining_hall/cancel_order', views.cancel_order, name="cancel_order"),
    path('dining_hall/student_preferences', views.student_preferences, name="student_preferences"),
    path('dining_hall/menu', views.student_menu_view, name='menu'),
    
    path('not_student/', views.not_student, name='not_student'),
]
