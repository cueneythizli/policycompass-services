# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, default='', blank=True)),
                ('text', models.TextField()),
                ('number', models.IntegerField()),
                ('issued', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator_path', models.CharField(max_length=1024)),
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChapterInContent',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('content', models.IntegerField()),
                ('story', models.ForeignKey(related_name='chapter_contents', to='storymanager.Chapter')),
            ],
            options={
                'verbose_name_plural': 'Chapter in Contents',
                'verbose_name': 'Chapter in Content',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('index', models.IntegerField()),
                ('issued', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator_path', models.CharField(max_length=1024)),
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('issued', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator_path', models.CharField(max_length=1024)),
            ],
            options={
                'ordering': ['-issued'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoryInChapter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('chapter', models.IntegerField()),
                ('story', models.ForeignKey(related_name='story_chapters', to='storymanager.Story')),
            ],
            options={
                'verbose_name_plural': 'Story in Chapters',
                'verbose_name': 'Story in Chapter',
            },
            bases=(models.Model,),
        ),
    ]
