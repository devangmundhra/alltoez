# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='yelp_url',
            field=models.URLField(null=True, verbose_name=b'Yelp Url', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=200, verbose_name=b'Venue name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='venue',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'Phone number, if available', max_length=128, verbose_name=b'Phone number', blank=True),
            preserve_default=True,
        ),
    ]
