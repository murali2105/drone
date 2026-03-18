from django.db import models
from django.contrib.auth.models import AbstractUser

class Drone(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('idle', 'Idle'),
        ('maintenance', 'Maintenance'),
        ('offline', 'Offline'),
    )

    drone_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idle')
    battery_level = models.IntegerField(default=100)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(default=0.0)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.drone_id})"

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=50, blank=True, null=True)
    assigned_drone = models.ForeignKey(Drone, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_users')

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

class PreCheckReport(models.Model):
    STATUS_CHOICES = (
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('warning', 'Warning'),
    )

    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name='pre_checks')
    submitted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='pre_checks')
    timestamp = models.DateTimeField(auto_now_add=True)
    checklist_data = models.JSONField(default=dict)
    overall_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Pre-Check: {self.drone.drone_id} by {self.submitted_by.username}"

class Mission(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    MISSION_TYPES = (
        ('survey', 'Survey Grid'),
        ('waypoint', 'Waypoint Route'),
        ('orbit', 'Orbit'),
        ('inspection', 'Inspection'),
    )

    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_missions')
    drone = models.ForeignKey(Drone, on_delete=models.SET_NULL, null=True, blank=True, related_name='missions')
    waypoints = models.JSONField(default=dict)
    mission_type = models.CharField(max_length=50, choices=MISSION_TYPES, default='waypoint')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    approved_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_missions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mission: {self.name} ({self.status})"

class FlightLog(models.Model):
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE, related_name='flight_log')
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name='flight_logs')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    max_altitude = models.FloatField(default=0.0)
    distance_flown = models.FloatField(default=0.0)

    def __str__(self):
        return f"Log: {self.mission.name} on {self.drone.drone_id}"
