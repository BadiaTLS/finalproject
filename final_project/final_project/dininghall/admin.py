from django.contrib import admin
from .models import table_session, table_booking_dininghall, table_time, table_live_booking

@admin.register(table_session)
class table_session_admin(admin.ModelAdmin):
    list_display = ("id", "date", "name", "menu")
    search_fields = ("date", "name", "menu")
    list_filter = ("date", "name")
    ordering = ("date",)

@admin.register(table_time)
class table_time_admin(admin.ModelAdmin):
    list_display = ("id", "time", "session_id", "display_session_name", "seat_limit", "available_seat")
    search_fields = ("time", "session_id__name")
    ordering = ("time",)

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['available_seat']
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ['available_seat']
        return []

    def display_session_name(self, obj):
        return obj.session_id.name
    
    display_session_name.short_description = "Session Name"

@admin.register(table_booking_dininghall)
class table_booking_dininghall_admin(admin.ModelAdmin):
    list_display = ['display_user_id', 'session_id', 'recommended_time', 'created_at']

    def display_user_id(self, obj):
        return obj.user_id.username if obj.user_id else None

    display_user_id.short_description = 'User ID'

@admin.register(table_live_booking)
class table_live_booking_admin(admin.ModelAdmin):
    list_display = ("id","arrival_time", "served_time", "depart_time", "bookings_id")
    search_fields = ("arrival_time", "served_time", "depart_time", "bookings_id")
    list_filter = ("arrival_time", "served_time", "depart_time")
    ordering = ("arrival_time",)
