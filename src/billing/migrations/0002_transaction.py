# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(max_length=256)),
                ('amount', models.DecimalField(max_digits=100, decimal_places=2)),
                ('card_type', models.CharField(max_length=256)),
                ('last_four', models.PositiveIntegerField(null=True, blank=True)),
                ('success', models.BooleanField(default=True)),
                ('transaction_status', models.CharField(max_length=256, null=True, blank=True)),
                ('order_id', models.CharField(max_length=256)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
