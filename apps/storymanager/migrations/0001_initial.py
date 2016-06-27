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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(default='', max_length=100, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('content', models.IntegerField()),
                ('story', models.ForeignKey(to='storymanager.Chapter', related_name='chapter_contents')),
            ],
            options={
                'verbose_name': 'Chapter in Content',
                'verbose_name_plural': 'Chapter in Contents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.IntegerField()),
                ('index', models.IntegerField()),
                ('stringIndex', models.IntegerField()),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('chapter', models.IntegerField()),
                ('story', models.ForeignKey(to='storymanager.Story', related_name='story_chapters')),
            ],
            options={
                'verbose_name': 'Story in Chapter',
                'verbose_name_plural': 'Story in Chapters',
            },
            bases=(models.Model,),
        ),
    ]
