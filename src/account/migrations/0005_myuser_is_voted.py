# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20160805_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_voted',
            field=models.BooleanField(default=False),
        ),
    ]
