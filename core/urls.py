from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'drones', views.DroneViewSet)
router.register(r'missions', views.MissionViewSet)

urlpatterns = [
    # Standard Web Views
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('map/', views.map_view, name='map_view'),
    path('pre-check/', views.pre_check_view, name='pre_check_view'),
    path('mission-planner/', views.mission_planner_view, name='mission_planner_view'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/pre-check/', views.submit_pre_check, name='api_submit_pre_check'),
]
