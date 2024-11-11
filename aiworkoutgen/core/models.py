from django.db import models
from django.contrib.auth.models import User

class WorkoutPlan(models.Model):
    WORKOUT_DURATIONS = [
        ('15', '15 minutes'),
        ('30', '30 minutes'),
        ('45', '45 minutes'),
        ('60', '60 minutes'),
        ('75', '75 minutes'),
        ('90', '90 minutes'),
    ]

    TARGET_AREAS = [
        ('Core/Abs', 'Core/Abs'),
        ('Legs', 'Legs'),
        ('Arms', 'Arms'),
        ('Full Body', 'Full Body'),
        ('Chest', 'Chest'),
        ('Back', 'Back'),
    ]

    EQUIPMENT_CHOICES = [
        ('Dumbbells', 'Dumbbells'),
        ('Barbell', 'Barbell'),
        ('Bench', 'Bench'),
        ('Squat Rack', 'Squat Rack'),
        ('Cables', 'Cables'),
        ('Bodyweight', 'Bodyweight'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    duration = models.CharField(max_length=15, choices=WORKOUT_DURATIONS)
    full_target_list = models.CharField(max_length=250, blank=True, null=True)  
    full_equipment_list = models.CharField(max_length=250, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False) #Will track if user completed field (T or F)
    workout_data = models.JSONField()  # Updated to use django.db.models.JSONField, workout_data
    
    # full list option here (testing)
    target_area = models.CharField(max_length=50, choices=TARGET_AREAS)
    equipment = models.CharField(max_length=50, choices=EQUIPMENT_CHOICES)
    custom_target = models.CharField(max_length=100, blank=True, null=True)
    custom_equipment = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s workout plan for {self.target_area} - {self.duration} mins"
    



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255, blank=True, null=True)  # Store the API key securely

    def __str__(self):
        return self.user.username
