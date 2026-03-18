from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Drone, PreCheckReport, Mission, FlightLog

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'student_id', 'assigned_drone')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('drone_id', 'name', 'model', 'status', 'battery_level', 'last_seen')
    list_filter = ('status', 'model')
    search_fields = ('drone_id', 'name')

@admin.register(PreCheckReport)
class PreCheckReportAdmin(admin.ModelAdmin):
    list_display = ('drone', 'submitted_by', 'overall_status', 'timestamp')
    list_filter = ('overall_status', 'timestamp')

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'drone', 'mission_type', 'status', 'created_at')
    list_filter = ('status', 'mission_type')
    search_fields = ('name',)

@admin.register(FlightLog)
class FlightLogAdmin(admin.ModelAdmin):
    list_display = ('mission', 'drone', 'start_time', 'end_time', 'distance_flown')
    list_filter = ('start_time', 'end_time')
