from django.db import models

# Create your models here.
class Greeting(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('Date published')
    likes = models.IntegerField(null=True)

    def __unicode__(self):
    	return self.title