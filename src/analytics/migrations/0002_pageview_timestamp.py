# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2016, 7, 26, 8, 31, 16, 114493, tzinfo=utc)),
        ),
    ]
