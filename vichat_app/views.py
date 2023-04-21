from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from .models import *
from .forms import *
import uuid
import boto3
import os
from decouple import config



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
   room = Chat_History.objects.get(slug=slug)
  #  messages = Chat_History.objects.filter(user1 = request.user, user2 = profile.user) | Chat_History.objects.filter( user1 = profile.user, user2 = request.user)
   messages = Message.objects.filter(room=room)[0:25]
  #  chatHistory = messages.first()

   return render(request, 'profile/details.html', {
      'profile': profile,
      'chatHistory': room      
   })


def friends_list(request):
  friends_list = request.user.friends.all()
  friend_profiles = Profile.objects.filter(user__in=friends_list)
  return render(request,'friends/index.html', {
      'friend_profiles': friend_profiles,
  })

def delete_friend(request, profile_id):
  other_user = Profile.objects.get(id=profile_id).user
  other_user.friends.remove(request.user.id)
  request.user.friends.remove(other_user.id)
  
  

  return redirect('friends_list')

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

def add_photo(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    # print(config('S3_BUCKET'))
    # print(f"{config('S3_BASE_URL')}{config('S3_BUCKET')}/{uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]}")
    print(photo_file)
    if photo_file:
        s3 = boto3.client('s3', 
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        bucket = config('S3_BUCKET')
        print(f'the bucket is {bucket}')
        print(key)
        try:
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{config('S3_BASE_URL')}{bucket}/{key}"
            Photo.objects.create(url=url, profile_id=profile_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('profile', profile_id=profile_id)

class ProfileUpdate(UpdateView):
   model = Profile
   fields = ['nickname']




