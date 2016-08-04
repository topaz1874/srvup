# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_auto_20160726_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageview',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
