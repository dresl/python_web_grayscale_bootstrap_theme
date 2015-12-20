# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brigade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brigade_title', models.CharField(max_length=200, verbose_name=b'N\xc3\xa1zev brig\xc3\xa1dy')),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 12, 20, 9, 30, 29, 782975, tzinfo=utc), verbose_name=b'Datum publikov\xc3\xa1n\xc3\xad')),
                ('rate', models.PositiveIntegerField(default=50, verbose_name=b'Za hodinu')),
                ('owner', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_day', models.CharField(default=b'Den: ', max_length=100, verbose_name=b'Po\xc5\x99ad\xc3\xad dne')),
                ('hours_per_day', models.PositiveIntegerField(default=None, verbose_name=b'Hodin denn\xc4\x9b')),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 12, 20, 9, 30, 29, 787766, tzinfo=utc), verbose_name=b'Datum publikov\xc3\xa1n\xc3\xad')),
                ('brigade', models.ForeignKey(to='mathematic.Brigade')),
            ],
        ),
    ]
