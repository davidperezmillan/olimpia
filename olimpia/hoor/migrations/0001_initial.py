# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-18 11:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hoor.submodels.models_ficha


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Capitulo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('temporada', models.IntegerField()),
                ('capitulo', models.IntegerField()),
                ('nombre', models.CharField(blank=True, max_length=200, null=True)),
                ('visto', models.NullBooleanField(default=False)),
                ('descargado', models.NullBooleanField(default=False)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Capitulos',
            },
        ),
        migrations.CreateModel(
            name='Descarga',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ep_start', models.CharField(blank=True, default='NRS00E00', max_length=8, null=True)),
                ('ep_end', models.CharField(blank=True, default='NRS99E99', max_length=8, null=True)),
                ('quality', models.CharField(choices=[('NR', 'Normal'), ('HD', 'High Definition'), ('VO', 'Version Original'), ('AL', 'Alternativo (Dificil busqueda)')], max_length=2)),
                ('ultima', models.DateTimeField(auto_now_add=True, null=True)),
                ('estado_descarga', models.NullBooleanField(default=False)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Descargas',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=100)),
                ('docfile', models.FileField(upload_to=hoor.submodels.models_ficha.user_directory_path)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('estado', models.IntegerField(choices=[(0, 'Descartada'), (1, 'Activa'), (2, 'Pendiente de nueva Temporada'), (3, 'Cancelada'), (4, 'Terminada')], default='0')),
                ('imagen', models.CharField(default='generico.jpg', max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fichas_autor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Fichas',
            },
        ),
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('file', models.CharField(blank=True, max_length=200, null=True)),
                ('clazz', models.CharField(blank=True, max_length=200, null=True)),
                ('active', models.NullBooleanField(default=False)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Plugins',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('plugins', models.ManyToManyField(to='hoor.Plugin')),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='TelegramChatIds',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idtelegram', models.IntegerField(blank=True, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('firstname', models.CharField(blank=True, max_length=200, null=True)),
                ('surname', models.CharField(blank=True, max_length=200, null=True)),
                ('group', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'telegram_chat_ids',
                'managed': True,
                'verbose_name_plural': 'telegramchatids',
            },
        ),
        migrations.CreateModel(
            name='TorrentServer',
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
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'TorrentServers',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hoor.TorrentServer'),
        ),
        migrations.AddField(
            model_name='profile',
            name='telegramCli',
            field=models.ManyToManyField(blank=True, to='hoor.TelegramChatIds'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='ficha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_ficha', to='hoor.Ficha'),
        ),
        migrations.AddField(
            model_name='descarga',
            name='ficha',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hoor.Ficha'),
        ),
        migrations.AddField(
            model_name='descarga',
            name='plugins',
            field=models.ManyToManyField(blank=True, to='hoor.Plugin'),
        ),
        migrations.AddField(
            model_name='capitulo',
            name='ficha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoor.Ficha'),
        ),
        migrations.AlterUniqueTogether(
            name='ficha',
            unique_together=set([('nombre',)]),
        ),
        migrations.AlterUniqueTogether(
            name='capitulo',
            unique_together=set([('ficha', 'temporada', 'capitulo')]),
        ),
    ]
