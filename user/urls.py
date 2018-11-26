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
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
]
