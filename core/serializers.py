from rest_framework import serializers
from .models import Drone, Mission, PreCheckReport, UserProfile

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role', 'student_id']

class PreCheckReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreCheckReport
        fields = '__all__'
        read_only_fields = ['submitted_by']

class MissionSerializer(serializers.ModelSerializer):
    drone_detail = DroneSerializer(source='drone', read_only=True)
    created_by_detail = UserProfileSerializer(source='created_by', read_only=True)

    class Meta:
        model = Mission
        fields = '__all__'
        read_only_fields = ['created_by', 'approved_by', 'status']
