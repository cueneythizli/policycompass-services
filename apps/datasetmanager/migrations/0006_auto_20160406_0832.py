# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasetmanager', '0005_remove_dataset_acronym'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetInSpatial',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('spatial', models.IntegerField()),
                ('dataset', models.ForeignKey(related_name='dataset_spatials', to='datasetmanager.Dataset')),
            ],
            options={
                'verbose_name': 'Dataset in Spatial',
                'verbose_name_plural': 'Dataset in Spatials',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='spatial',
        ),
    ]
