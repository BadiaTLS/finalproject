from django.contrib import admin
from .models import table_students_information

@admin.register(table_students_information)
class table_students_information_admin(admin.ModelAdmin):
    list_display = ("nim", "name", "study_program", "batch_year", "username")
    search_fields = ("nim", "name", "study_program", "batch_year", "username")
    list_filter = ("study_program", "batch_year")
    ordering = ("name",)
