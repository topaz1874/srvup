# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='comment.Comment', null=True),
        ),
    ]
