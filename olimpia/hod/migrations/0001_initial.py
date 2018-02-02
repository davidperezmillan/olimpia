# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-02 11:54
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
            name='Capitulos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('temporada', models.IntegerField()),
                ('capitulos', models.IntegerField()),
                ('nombre', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Capitulos',
            },
        ),
        migrations.CreateModel(
            name='Fichas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('estado', models.CharField(choices=[('0', 'Pendiente nueva temporada'), ('1', 'Activa'), ('2', 'Cancelada')], default='0', max_length=2)),
                ('imagen', models.CharField(default='generico.jpg', max_length=200)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'fichas',
            },
        ),
        migrations.CreateModel(
            name='Vistos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('capitulo', models.IntegerField()),
                ('visto', models.NullBooleanField(default=False)),
                ('descargado', models.NullBooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vistos_autor', to=settings.AUTH_USER_MODEL)),
                ('temporada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hod.Capitulos')),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Vistos',
            },
        ),
        migrations.AlterUniqueTogether(
            name='fichas',
            unique_together=set([('nombre', 'estado')]),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='ficha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hod.Fichas'),
        ),
        migrations.AlterUniqueTogether(
            name='vistos',
            unique_together=set([('author', 'temporada', 'capitulo')]),
        ),
        migrations.AlterUniqueTogether(
            name='capitulos',
            unique_together=set([('ficha', 'temporada')]),
        ),
    ]
