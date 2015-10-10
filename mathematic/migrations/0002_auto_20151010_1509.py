# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mathematic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brigade',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 10, 13, 9, 42, 887672, tzinfo=utc), verbose_name=b'Datum publikov\xc3\xa1n\xc3\xad'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='day',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 10, 13, 9, 42, 888240, tzinfo=utc), verbose_name=b'Datum publikov\xc3\xa1n\xc3\xad'),
            preserve_default=True,
        ),
    ]
