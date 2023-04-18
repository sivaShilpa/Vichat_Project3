from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)


    def __str__(self):
        return f"{self.username} | {self.friends}"

class Profile(models.Model):
    nickname = models.CharField(max_length=50)
    profile_pic = models.CharField(max_length=400)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

class Friend_Request(models.Model):
    from_user = models.ForeignKey(
      User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
      User, related_name='to_user', on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#this method to update profile when user is updated
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()