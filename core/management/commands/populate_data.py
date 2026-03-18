from django.core.management.base import BaseCommand
from core.models import UserProfile, Drone

class Command(BaseCommand):
    help = 'Populates the database with initial test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # Create Admin
        if not UserProfile.objects.filter(username='admin').exists():
            UserProfile.objects.create_superuser('admin', 'admin@example.com', 'adminpass', role='admin')
            self.stdout.write(self.style.SUCCESS('Admin user created (admin / adminpass)'))

        # Create Drones
        d1, _ = Drone.objects.get_or_create(
            drone_id='Alpha-01', defaults={'name': 'Scout 1', 'model': 'DJI Mavic 3 Enterprise', 'status': 'active', 'lat': 37.7749, 'lng': -122.4194, 'altitude': 120}
        )
        d2, _ = Drone.objects.get_or_create(
            drone_id='Beta-09', defaults={'name': 'Heavy Lift 1', 'model': 'DJI Matrice 350 RTK', 'status': 'maintenance', 'battery_level': 45}
        )
        d3, _ = Drone.objects.get_or_create(
            drone_id='Gamma-42', defaults={'name': 'Survey 1', 'model': 'Autel EVO Max 4T', 'status': 'idle'}
        )
        
        self.stdout.write(self.style.SUCCESS('Drones created'))

        # Create Student
        if not UserProfile.objects.filter(username='student1').exists():
            student = UserProfile.objects.create_user('student1', 'student1@example.com', 'studentpass')
            student.role = 'student'
            student.student_id = 'ST-9001'
            student.assigned_drone = d1
            student.save()
            self.stdout.write(self.style.SUCCESS('Student user created (student1 / studentpass) assigned to Alpha-01'))

        self.stdout.write(self.style.SUCCESS('Data population complete.'))
