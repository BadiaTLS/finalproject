from django.contrib import admin
from .models import table_menu, table_booking_dininghall, table_time
# Register your models here.


@admin.register(table_menu)
class table_menu_admin(admin.ModelAdmin):
    list_display = ("date", "session", "menu", "limit")
    search_fields = ("date", "session", "menu")
    list_filter = ("date", "session")
    ordering = ("date",)

    def get_exclude(self, request, obj=None):
        if obj is None:  # Only exclude the 'limit' field when adding new data
            return ['available']
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:  # Make the 'limit' field readonly when editing existing data
            return ['available']
        return []

@admin.register(table_time)
class table_time_admin(admin.ModelAdmin):
    list_display = ("id", "time",)
    search_fields = ("time",)
    ordering = ("time",)

@admin.register(table_booking_dininghall)
class table_booking_dininghall_admin(admin.ModelAdmin):
    list_display = ['display_students_nim', 'time_booked', 'menu', 'available', 'created_at']

    def display_students_nim(self, obj):
        return obj.students_nim.nim if obj.students_nim else None

    display_students_nim.short_description = 'Students NIM'
