# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('client_ip', models.GenericIPAddressField(null=True)),
                ('action', models.CharField(max_length=50, choices=[(b'convert', b'Convert'), (b'download', b'Download')])),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('youtube_id', models.CharField(unique=True, max_length=100)),
                ('url', models.URLField(max_length=255)),
                ('title', models.TextField()),
                ('duration', models.IntegerField(null=True)),
                ('audio_filename', models.CharField(max_length=255, null=True, blank=True)),
                ('audio_filesize', models.IntegerField(null=True)),
                ('download_count', models.IntegerField(default=0, null=True)),
                ('last_download_date', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='activitylog',
            name='video',
            field=models.ForeignKey(to='downloader.Video'),
        ),
    ]
