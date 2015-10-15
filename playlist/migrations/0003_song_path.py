# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0002_auto_20150908_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='path',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
