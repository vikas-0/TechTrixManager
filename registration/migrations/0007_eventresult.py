# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 04:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_eventregistration'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participated', models.BooleanField(default=False)),
                ('score', models.DecimalField(decimal_places=4, max_digits=10)),
                ('status', models.CharField(default='Not participated yet', max_length=100)),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='registration.EventRegistration')),
            ],
        ),
    ]
