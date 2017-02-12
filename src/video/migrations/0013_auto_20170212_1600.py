# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('video', '0012_video_like_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voteuser', models.CharField(max_length=256)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.RemoveField(
            model_name='video',
            name='like_user',
        ),
        migrations.AlterField(
            model_name='video',
            name='likes',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
