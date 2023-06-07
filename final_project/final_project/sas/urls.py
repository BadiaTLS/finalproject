from django.urls import path
from . import views

urlpatterns = [
    path('', views.sas_index, name='sas_index'),
    path('import_student', views.import_student, name='import_student'),
    path('import_class', views.import_class, name='import_class'),
    path('not_sas', views.not_sas, name='not_sas'),
]
