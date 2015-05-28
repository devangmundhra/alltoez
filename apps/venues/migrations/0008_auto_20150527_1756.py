# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0007_venue_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='neighborhood',
            field=models.CharField(help_text='Neighborhood/rough area of venue. Leave blank for auto-fill', max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
