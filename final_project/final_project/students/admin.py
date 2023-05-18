from django.contrib import admin
from .models import table_students_information, table_classes
# Register your models here.


@admin.register(table_students_information)
class table_students_information_admin(admin.ModelAdmin):
    list_display = ("nim", "name", "study_program", "batch_year", "username")
    search_fields = ("nim", "name", "study_program", "batch_year", "username")
    list_filter = ("study_program", "batch_year")
    ordering = ("name",)

@admin.register(table_classes)
class table_classes_admin(admin.ModelAdmin):
    list_display = ("class_code", "class_name", "class_date", "class_start", "class_end", "attendes")
    search_fields = ("class_code", "class_name", "class_date", "class_start", "class_end")
    list_filter = ("class_date", "class_start", "class_end")
    ordering = ("class_date",)