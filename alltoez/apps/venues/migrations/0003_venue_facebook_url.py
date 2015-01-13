# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_auto_20141230_0636'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='facebook_url',
            field=models.URLField(null=True, verbose_name=b'Facebook Url', blank=True),
            preserve_default=True,
        ),
    ]
