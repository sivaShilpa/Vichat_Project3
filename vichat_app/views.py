from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random
import time
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

   messages = Chat_History.objects.filter(user1 = request.user, user2 = profile.user) | Chat_History.objects.filter( user1 = profile.user, user2 = request.user)

   chatHistory = messages.first()

   return render(request, 'profile/details.html', {
      'profile': profile,
      'chatHistory': chatHistory
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

        c = Chat_History.objects.create(
           user1=friend_request.from_user,
           user2=friend_request.to_user,
           roomcode=f"{friend_request.to_user.username}{friend_request.from_user.username}"
           )
        c.save()

        friend_request.delete()
        return redirect('fr-index')
    else:
        return redirect('fr-index')

def add_photo(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    my_profile = Profile.objects.get(id=profile_id)
  
    
    if photo_file:
        s3 = boto3.client('s3', 
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        bucket = config('S3_BUCKET')
        
        try:
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{config('S3_BASE_URL')}{bucket}/{key}"
            Photo.objects.create(url=url, profile_id=profile_id)
            my_profile.profile_pic = url
            my_profile.save()
    
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('profile', profile_id=profile_id)


def get_token(request):
    appId = config('APP_ID')
    appCertificate = config('APP_CERT')
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)

    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)

def room(request):
   return render(request, 'vichat_app/room.html')



class ProfileUpdate(UpdateView):
   model = Profile
   fields = ['nickname']




