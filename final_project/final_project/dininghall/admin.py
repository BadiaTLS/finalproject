from django.contrib import admin
from .models import table_menu, table_booking_dininghall, table_time#, table_staff_information
from final_project.accounts.models import CustomUser
# Register your models here.


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
        return obj.students_nim.nim if obj.students_nim else None

    display_students_nim.short_description = 'Students NIM'
