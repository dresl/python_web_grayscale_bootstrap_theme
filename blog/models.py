from django.db import models
from time import time
from django.utils import timezone
from django.contrib.auth.models import User

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('Date published', default=timezone.now())
    thumbnail = models.FileField(blank=True, null=True, upload_to=get_upload_file_name)
    users_like_it = models.ManyToManyField(User, blank=True, null=True)
    def __unicode__(self):
	return self.title
