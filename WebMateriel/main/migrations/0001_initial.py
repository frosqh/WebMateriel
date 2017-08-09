# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default=b'-------------------------', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default=b'Famille', max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default=b'Fournisseur', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HistoLigne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('stockChange', models.CharField(default=b'', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Outil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default=b'Outil', max_length=75)),
                ('numSerie', models.CharField(default=b'', max_length=25)),
                ('isDispo', models.BooleanField(default=True)),
                ('autreId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Autre')),
            ],
        ),
        migrations.CreateModel(
            name='Pignouf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default=b'Nom', max_length=50)),
                ('prenom', models.CharField(default=b'Prenom', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SousFamille',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default=b'Sous-Famille', max_length=75)),
                ('familleID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Famille')),
            ],
        ),
        migrations.AddField(
            model_name='outil',
            name='emprunteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Pignouf'),
        ),
        migrations.AddField(
            model_name='outil',
            name='famille',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.Famille'),
        ),
        migrations.AddField(
            model_name='outil',
            name='fournisseurID',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.Fournisseur'),
        ),
        migrations.AddField(
            model_name='outil',
            name='sousfamille',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.SousFamille'),
        ),
        migrations.AddField(
            model_name='histoligne',
            name='pignoufID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Pignouf'),
        ),
        migrations.AddField(
            model_name='histoligne',
            name='productID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Outil'),
        ),
    ]