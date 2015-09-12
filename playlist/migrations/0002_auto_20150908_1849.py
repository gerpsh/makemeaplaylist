# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='artist_familiarty',
            new_name='artist_familiarity',
        ),
        migrations.AlterField(
            model_name='song',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='tempo',
            field=models.IntegerField(null=True),
        ),
    ]
