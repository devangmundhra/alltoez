# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0003_venue_facebook_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='slug',
            field=models.SlugField(null=True, blank=True, help_text=b'The part of the name (if provided) that is used in the url.                             Leave this blank if you want the system to generate one for you.', unique=True),
            preserve_default=True,
        ),
    ]
