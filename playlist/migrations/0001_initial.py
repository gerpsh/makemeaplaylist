# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('artist', models.CharField(max_length=200)),
                ('song_hotness', models.DecimalField(null=True, max_digits=12, decimal_places=11)),
                ('artist_hotness', models.DecimalField(null=True, max_digits=12, decimal_places=11)),
                ('artist_familiarty', models.DecimalField(null=True, max_digits=12, decimal_places=11)),
                ('danceability', models.DecimalField(null=True, max_digits=12, decimal_places=11)),
                ('duration', models.DecimalField(null=True, max_digits=12, decimal_places=11)),
                ('energy', models.DecimalField(null=True, max_digits=12, decimal_places=11)),
                ('tempo', models.DecimalField(null=True, max_digits=12, decimal_places=11)),
            ],
            options={
                'ordering': ('artist', 'title'),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('artist', 'title')]),
        ),
    ]
