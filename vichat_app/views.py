from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.

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
        return HTTPResponse('Friend request sent!')
    else:
        return HTTPResponse('Friend request was already sent')

@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HTTPResponse('friend request accepted')
    else:
        return HTTPResponse('friend request not accepted')


