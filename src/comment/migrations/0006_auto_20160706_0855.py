# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20160704_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
