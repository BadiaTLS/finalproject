from django.contrib import admin
from .models import table_staff_information, table_menu, table_booking_dininghall, table_time
# Register your models here.

@admin.register(table_staff_information)
class table_staff_information_admin(admin.ModelAdmin):
    list_display = ("id", "name", "position", "username")
    search_fields = ("name", "position", "username")
    list_filter = ("position",)
    ordering = ("name",)

@admin.register(table_menu)
class table_menu_admin(admin.ModelAdmin):
    list_display = ("date", "session", "menu", "vacancy")
    search_fields = ("date", "session", "menu")
    list_filter = ("date", "session")
    ordering = ("date",)

@admin.register(table_time)
class table_time_admin(admin.ModelAdmin):
    list_display = ("id", "time",)
    search_fields = ("time",)
    ordering = ("time",)

@admin.register(table_booking_dininghall)
class table_booking_dininghall_admin(admin.ModelAdmin):
    list_display = ['display_students_nim', 'time_booked', 'menu', 'vacancy', 'created_at']
    def display_students_nim(self, obj):
        return [student.nim for student in obj.students_nim.all()]
    display_students_nim.short_description = 'Students NIM'
    list_filter = ['time_booked', 'created_at']
    search_fields = ['students_nim__nim']