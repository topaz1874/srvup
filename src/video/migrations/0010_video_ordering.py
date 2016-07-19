# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_auto_20160708_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='ordering',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
