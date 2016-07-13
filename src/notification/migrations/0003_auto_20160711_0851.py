# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20160711_0733'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NotificationManager',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='read',
        ),
    ]
