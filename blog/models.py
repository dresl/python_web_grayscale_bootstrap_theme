# encoding: utf-8
from django.db import models
from time import time
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('Zveřejněno', default=timezone.now())
    thumbnail = models.FileField(blank=True, null=True, upload_to=get_upload_file_name)
    users_like_it = models.ManyToManyField(User, blank=True, null=True)
    def __unicode__(self):
	return self.title

class Comment(models.Model):
	owner = models.ForeignKey(User, verbose_name="Vlastník", blank=True, null=True)
	blog = models.ForeignKey(Blog, blank=True, null=True)
	comment = models.CharField(max_length=500, verbose_name="Komentář", blank=True, null=True)
	pub_date = models.DateTimeField(verbose_name="Zveřejněno", default=datetime.datetime.now(), blank=True, null=True)
	def __unicode__(self):
		return str(self.blog)