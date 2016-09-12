# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_usermerchantid'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermerchantid',
            name='plan_id',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='usermerchantid',
            name='subscription_id',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
    ]
