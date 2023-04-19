from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from .models import *
from .forms import *

# Create your views here.
@login_required
def main(request):
   friends_list = request.user.friends.all()
   friend_profiles = Profile.objects.filter(user__in=friends_list)

   return render(request, 'vichat_app/main.html', {
      'friend_profiles': friend_profiles,
   })

def profile(request, profile_id):
   profile = Profile.objects.get(id=profile_id)
   return render(request, 'profile/details.html', {
      'profile': profile,
   })

def friends_list(request):
  friends_list = request.user.friends.all()
  friend_profiles = Profile.objects.filter(user__in=friends_list)
  return render(request,'friends/index.html', {
      'friend_profiles': friend_profiles,
  })

def friend_requests_index(request):
  allusers = User.objects.all()
  all_friend_requests = Friend_Request.objects.filter(to_user = request.user)
  friends_list = request.user.friends.all()

  return render(request, 'profile/friend_requests/index.html', {
      'all_friend_requests': all_friend_requests,
      'allusers': allusers,
      'friends_list': friends_list,
  })

def signup(request):
  error_message = ''
  if request.method == 'POST':

    form = SignupForm(request.POST)
    if form.is_valid():
    
      user = form.save()
  
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'

  form = SignupForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
      from_user=from_user, to_user=to_user)
    if created:
        return redirect('fr-index')
    else:
        return redirect('fr-index')

@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return redirect('fr-index')
    else:
        return redirect('fr-index')
    

class ProfileUpdate(UpdateView):
   model = Profile
   fields = ['nickname', 'profile_pic']



