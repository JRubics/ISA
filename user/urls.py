from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login_submit, name='login_submit'),
    path('register/', views.registration_submit, name='registration_submit'),
    path('logout/', views.logout_submit, name='logout_submit'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('confirm/<username>/', views.confirm, name='confirm'),

    #filip dodao
    path('profile', views.profile, name='profile'),
    path('profile/pass_change/', views.change_password, name='profile_pass_change'),
    path('profile/edit/', views.ProfileEdit.as_view(), name='profile_edit'),
    path('profile/people_list', views.ListProfiles.as_view(), name='profile_people_list'),
    path('profile/friend_requests', views.ListFriendRequests.as_view(), name='profile_friend_requests'),
    path('profile/unfriend', views.Unfriend.as_view(), name='profile_unfriend'),
    path('profile/invitations', views.Invitation.as_view(), name='profile_initations'),


    #boris dodao
    path('first_login/', views.first_login, name='first_login'),

    path('cancel/reservation', views.cancel_reservation, name='cancel_reservation'),
]