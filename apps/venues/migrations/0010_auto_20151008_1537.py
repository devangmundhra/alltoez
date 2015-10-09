# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0009_auto_20151008_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='state',
            field=models.CharField(db_index=True, max_length=150, null=True, blank=True),
        ),
    ]
