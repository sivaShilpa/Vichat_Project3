from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.


class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)


    def __str__(self):
        return f"{self.username} | {self.friends}"

class Profile(models.Model):
    nickname = models.CharField(max_length=50)
    profile_pic = models.CharField(max_length=400)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_id': self.id})
    

class Friend_Request(models.Model):
    from_user = models.ForeignKey(
      User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
      User, related_name='to_user', on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, nickname=instance.username)

#this method to update profile when user is updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000) 

class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Photo for user: {self.profile.user} @{self.url}"
    
class Chat_History(models.Model):
    user1 = models.ForeignKey(
      User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(
      User, related_name='user2', on_delete=models.CASCADE)
    
    msg_history = models.ForeignKey(Message, on_delete=models.CASCADE)

