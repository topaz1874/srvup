# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_auto_20170212_1600'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='voteuser',
            unique_together=set([('voteuser', 'content_type', 'object_id')]),
        ),
    ]
