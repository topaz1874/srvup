# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_myuser_is_voted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='is_voted',
        ),
    ]
