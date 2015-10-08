# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0008_auto_20150527_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='country',
            field=django_countries.fields.CountryField(default='US', max_length=2, blank=True, null=True, db_index=True),
        ),
    ]
