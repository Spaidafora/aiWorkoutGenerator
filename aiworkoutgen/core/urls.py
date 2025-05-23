from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL for the 'home' view
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),    
    path('signup', views.user_signup, name='signup'),
    path('workout', views.generate_workout, name='workout'),
    path('history', views.display_workout_history, name='history'),
    path('home', views.save_workout, name='save_workout'),
    path('delete_workout/<int:pk>', views.delete_workout, name='delete_workout'),  # Primary key reference > workout ID
      path('profile', views.user_profile, name='user_profile'),  # Profile path
]
