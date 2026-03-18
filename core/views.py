from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Drone, Mission, PreCheckReport, FlightLog, UserProfile
from .serializers import DroneSerializer, MissionSerializer, PreCheckReportSerializer

# --- Authentication & Standard Views ---

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# Role check decorators
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access Denied: Admins Only")
    return wrap

def student_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'student':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access Denied: Students Only")
    return wrap

@login_required
def map_view(request):
    return render(request, 'map.html')

@login_required
@student_required
def student_dashboard(request):
    # Pass user stats
    return render(request, 'student_dashboard.html')

@login_required
@admin_required
def admin_dashboard(request):
    # Fleet stats
    drones = Drone.objects.all()
    active_count = drones.filter(status='active').count()
    idle_count = drones.filter(status='idle').count()
    maintenance_count = drones.filter(status='maintenance').count()
    
    return render(request, 'admin_dashboard.html', {
        'total_drones': drones.count(),
        'active_count': active_count,
        'idle_count': idle_count,
        'maintenance_count': maintenance_count
    })

@login_required
def pre_check_view(request):
    return render(request, 'pre_check.html')

@login_required
def mission_planner_view(request):
    return render(request, 'mission_planner.html')

# --- DRF API Views ---

class DroneViewSet(viewsets.ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    permission_classes = [permissions.IsAuthenticated]

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Students only see their own missions or missions for their assigned drone
        if self.request.user.role == 'student':
            return Mission.objects.filter(created_by=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_pre_check(request):
    serializer = PreCheckReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(submitted_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
