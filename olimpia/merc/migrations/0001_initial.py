# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-12 09:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plugins',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('file', models.CharField(blank=True, max_length=200, null=True)),
                ('clazz', models.CharField(blank=True, max_length=200, null=True)),
                ('active', models.NullBooleanField(default=False)),
            ],
            options={
                'db_table': 'plugins',
                'managed': True,
                'verbose_name_plural': 'Plugins',
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('ep_start', models.CharField(blank=True, default='NRS00E00', max_length=8, null=True)),
                ('ep_end', models.CharField(blank=True, default='NRS99E99', max_length=8, null=True)),
                ('quality', models.CharField(default='NR', max_length=2)),
                ('ultima', models.DateTimeField(auto_now_add=True, null=True)),
                ('paussed', models.NullBooleanField(default=False)),
                ('skipped', models.NullBooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='series_autor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'series',
                'managed': True,
                'verbose_name_plural': 'series',
            },
        ),
        migrations.CreateModel(
            name='TelegramChatIds',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('firstname', models.CharField(blank=True, max_length=200, null=True)),
                ('surname', models.CharField(blank=True, max_length=200, null=True)),
                ('group', models.CharField(blank=True, max_length=200, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='telegram_chat_ids_autor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'telegram_chat_ids',
                'managed': True,
                'verbose_name_plural': 'telegram_chat_ids',
            },
        ),
        migrations.CreateModel(
            name='TorrentServers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('torrent_active', models.NullBooleanField(default=False)),
                ('space_disk', models.IntegerField()),
                ('host', models.CharField(blank=True, max_length=200, null=True)),
                ('port', models.IntegerField()),
                ('user', models.CharField(blank=True, max_length=200, null=True)),
                ('password', models.CharField(blank=True, max_length=200, null=True)),
                ('paused', models.NullBooleanField(default=False)),
                ('download', models.CharField(blank=True, max_length=200, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='torrentservers_autor', to=settings.AUTH_USER_MODEL)),
                ('plugins', models.ManyToManyField(blank=True, to='merc.Plugins')),
            ],
            options={
                'db_table': 'torrentservers',
                'managed': True,
                'verbose_name_plural': 'TorrentServers',
            },
        ),
        migrations.AlterUniqueTogether(
            name='series',
            unique_together=set([('nombre', 'quality', 'author')]),
        ),
    ]