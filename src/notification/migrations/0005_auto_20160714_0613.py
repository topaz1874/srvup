# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0004_auto_20160711_0853'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifications',
            options={'ordering': ['timestamp']},
        ),
    ]
