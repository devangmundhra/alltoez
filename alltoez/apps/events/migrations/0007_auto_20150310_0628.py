# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import media_field.db


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_similarevents'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='image',
            new_name='image_info',
        ),
        migrations.AddField(
            model_name='event',
            name='img',
            field=media_field.db.MediaField(default='invalid', upload_to='events_media'),
            preserve_default=False,
        ),
    ]
