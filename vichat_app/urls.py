from django.urls import path
from . import views


urlpatterns =[
    path('accounts/signup/', views.signup, name='signup'),
    path('send_friend_request/<int:userID>/',
    views.send_friend_request, name='send friend request'),
    path('accept_friend_request/<int:requestID>/', 
    views.accept_friend_request, name='accept friend request'),
]