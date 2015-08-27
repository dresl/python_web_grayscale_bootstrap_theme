# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import blog.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 8, 27, 9, 24, 35, 125136, tzinfo=utc), verbose_name=b'Date published')),
                ('likes', models.IntegerField(default=0)),
                ('thumbnail', models.FileField(null=True, upload_to=blog.models.get_upload_file_name, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
