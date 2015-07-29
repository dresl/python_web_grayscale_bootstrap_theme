import datetime
from django.db import models
from django.utils import timezone
from django import forms
from time import time

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    def __unicode__(self):              # __unicode__ on Python 2 ; __str__ on Python 3
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):              # __unicode__ on Python 2 ; __str__ on Python 3
        return self.choice_text

class Sidebar(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('Date published')

    def __unicode__(self):
        return self.title

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)

class Greeting(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('Date published', default=timezone.now())
    likes = models.IntegerField(default=0)
    thumbnail = models.FileField(blank=True, null=True, upload_to=get_upload_file_name)

    def __unicode__(self):
        return self.title
