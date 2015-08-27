# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brigade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brigade_title', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 8, 27, 9, 24, 35, 115905, tzinfo=utc), verbose_name=b'Datum publikov\xc3\xa1n\xc3\xad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_day', models.CharField(default=b'Den: ', max_length=100, verbose_name=b'Po\xc5\x99ad\xc3\xad dne')),
                ('hours_per_day', models.PositiveIntegerField(default=0, verbose_name=b'Hodin denn\xc4\x9b')),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 8, 27, 9, 24, 35, 117094, tzinfo=utc), verbose_name=b'Datum publikov\xc3\xa1n\xc3\xad')),
                ('brigade', models.ForeignKey(to='mathematic.Brigade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
