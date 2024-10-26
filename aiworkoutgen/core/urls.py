from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), #  Root URL for the 'home' view
    path('login', views.user_login, name='login'),    
    path('signup', views.user_signup, name='signup'),
    path('workout', views.generate_workout, name='workout'),
    path('history', views.display_workout_history, name='history'),
    path('home', views.save_workout, name='save_workout'),
    path('delete_workout/<int:pk>', views.delete_workout, name='delete_workout'), #primary key ref > workout id
]
