from django.urls import path, include
from . import views


urlpatterns =[
    path('profile/', views.profile, name='profile'),
    path('profile/friend_requests/', views.friend_requests_index, name='fr-index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('send_friend_request/<int:userID>/',
    views.send_friend_request, name='send friend request'),
    path('accept_friend_request/<int:requestID>/', 
    views.accept_friend_request, name='accept friend request'),
]