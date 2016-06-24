# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'uploads/%Y/%m/%d', blank=True)),
                ('upload_vid', models.FileField(null=True, upload_to=b'uploads/%Y/%m/%d', blank=True)),
                ('embed_code', models.CharField(max_length=500, null=True, blank=True)),
            ],
        ),
    ]
