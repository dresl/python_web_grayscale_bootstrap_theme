# encoding: utf-8
from django.utils import timezone
from time import time
import datetime
from django.db import models

class Brigade(models.Model):
    brigade_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Datum publikování', default=timezone.now())
    def __unicode__(self):              # __unicode__ on Python 2 ; __str__ on Python 3
        return self.brigade_title
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Day(models.Model):
	brigade = models.ForeignKey(Brigade)
	number_of_day = models.CharField(max_length=100, verbose_name="Pořadí dne", default='Den: ')
	hours_per_day = models.PositiveIntegerField(verbose_name="Hodin denně", default=None)
	pub_date = models.DateTimeField('Datum publikování', default=timezone.now())
	def __unicode__(self):              # __unicode__ on Python 2 ; __str__ on Python 3
	    return self.number_of_day