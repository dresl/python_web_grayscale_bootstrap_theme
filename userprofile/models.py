from django.db import models
from django.utils import timezone
import datetime
from django import forms
from time import time
from mathematic.models import Brigade, Day
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def get_upload_file_name(instance, filename):
    return "uploaded_files/profile_pictures/%s_%s" % (str(time()).replace('.', '_'), filename)

class UserProfile(models.Model):  
    user = models.OneToOneField(User, related_name="profile")
    hobbies = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.FileField(blank=True, null=True, upload_to=get_upload_file_name)
    #other fields here

    def __unicode__(self):  
          return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)