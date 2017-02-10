# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0010_video_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='likes',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
