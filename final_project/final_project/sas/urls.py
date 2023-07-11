from django.urls import path
from . import views

urlpatterns = [
    path('', views.sas_index, name='sas_index'),
    path('import_user', views.import_user, name='import_user'),
    path('import_class', views.import_class, name='import_class'),
    path('not_sas', views.not_sas, name='not_sas'),
    path('upload/', views.upload_file, name='upload_file'),
    path('delete_all_class/', views.delete_all_class_view, name='delete_all_class'),

]
