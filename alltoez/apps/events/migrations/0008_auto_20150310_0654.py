# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150310_0628'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='img',
            new_name='image',
        ),
    ]
