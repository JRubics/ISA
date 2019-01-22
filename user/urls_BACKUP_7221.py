from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login_submit, name='login_submit'),
    path('register/', views.registration_submit, name='registration_submit'),
    path('logout/', views.logout_submit, name='logout_submit'),
    path('home/', views.home, name='home'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('confirm/<username>/', views.confirm, name='confirm'),
<<<<<<< HEAD
    path('reservations', views.reservations, name='reservations'),

    #filip dodao
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
]
=======
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
]
>>>>>>> 00c753c144a21150869dc1738cd557b0b0893ad8
