# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import blog.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 12, 24, 9, 12, 22, 772897, tzinfo=utc), verbose_name=b'Zve\xc5\x99ejn\xc4\x9bno')),
                ('thumbnail', models.FileField(null=True, upload_to=blog.models.get_upload_file_name, blank=True)),
                ('users_like_it', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=500, null=True, verbose_name=b'Koment\xc3\xa1\xc5\x99', blank=True)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 12, 24, 10, 12, 22, 774320), null=True, verbose_name=b'Zve\xc5\x99ejn\xc4\x9bno', blank=True)),
                ('blog', models.ForeignKey(blank=True, to='blog.Blog', null=True)),
                ('owner', models.ForeignKey(verbose_name=b'Vlastn\xc3\xadk', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
