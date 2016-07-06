# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20160701_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='level',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, to='comment.Comment', null=True),
        ),
    ]
