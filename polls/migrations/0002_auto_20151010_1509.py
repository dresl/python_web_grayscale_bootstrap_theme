# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greeting',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 10, 13, 9, 42, 891821, tzinfo=utc), verbose_name=b'Date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 10, 13, 9, 42, 890328, tzinfo=utc), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
