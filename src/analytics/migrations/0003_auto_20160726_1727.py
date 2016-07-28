# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('analytics', '0002_pageview_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='primary_content_type',
            field=models.ForeignKey(related_name='primary_obj', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='pageview',
            name='primary_object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pageview',
            name='secondary_content_type',
            field=models.ForeignKey(related_name='secondary_obj', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='pageview',
            name='secondary_object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2016, 7, 26, 9, 27, 26, 372629, tzinfo=utc)),
        ),
    ]
