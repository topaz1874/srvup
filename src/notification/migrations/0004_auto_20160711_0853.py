# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20160711_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='unread',
        ),
        migrations.AddField(
            model_name='notifications',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
