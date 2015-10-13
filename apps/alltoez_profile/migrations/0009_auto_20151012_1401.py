# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('alltoez_profile', '0008_auto_20151008_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=django_countries.fields.CountryField(default='US', max_length=2, db_index=True),
        ),
    ]
