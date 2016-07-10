# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_taggeditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.SlugField(choices=[(b'django', b'django'), (b'python', b'python'), (b'pycon', b'pycon'), (b'css', b'css'), (b'bootstrap', b'bootstrap'), (b'content_types', b'content_types')]),
        ),
    ]
