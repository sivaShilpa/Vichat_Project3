from django.urls import path, include
from . import views


urlpatterns =[
    path('profile/friend_requests/', views.friend_requests_index, name='fr-index'),
    path('profile/<int:profile_id>', views.profile, name='profile'),
    path('profile/<int:pk>/update', views.ProfileUpdate.as_view(), name='profile_update'),

    path('accounts/signup/', views.signup, name='signup'),

    path('send_friend_request/<int:userID>/',
    views.send_friend_request, name='send friend request'),
    path('accept_friend_request/<int:requestID>/', 
    views.accept_friend_request, name='accept friend request'),

    path('', views.main, name='main'),

    path('users/friends/<int:profile_id>/delete', views.delete_friend, name='remove_friend'),
    path('user/friends', views.friends_list, name='friends_list'),
]