# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base', models.CharField(default=b'nobase', max_length=500)),
                ('isapre', models.CharField(default=b'noisapre', max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base', models.CharField(default=b'nobase', max_length=500)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('region', models.CharField(default=b'noregion', max_length=50)),
                ('commune', models.CharField(default=b'nocommune', max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=50)),
                ('typemath', models.CharField(default=b'notypemath', max_length=50)),
                ('math', models.CharField(default=b'nomath', max_length=1000)),
                ('status', models.CharField(default=b'incomplete', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('buy', models.CharField(default=b'0', max_length=50)),
                ('description', models.CharField(default=b'nodescription', max_length=1000)),
                ('gr', models.CharField(default=b'0', max_length=50)),
                ('it', models.CharField(default=b'0', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='clients_vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_vendor', models.CharField(default=b'noid_vendor', max_length=500)),
                ('id_client', models.CharField(default=b'noid_client', max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base', models.CharField(default=b'nobase', max_length=500)),
                ('base_login', models.CharField(default=b'nobase_login', max_length=500)),
                ('name', models.CharField(default=b'noname', max_length=50)),
                ('phone', models.CharField(default=b'nophone', max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('coins_avaiable', models.CharField(default=b'0', max_length=50)),
                ('coins_used', models.CharField(default=b'0', max_length=50)),
                ('user', models.CharField(default=b'nouser', max_length=50)),
                ('psw', models.CharField(default=b'nopsw', max_length=1000)),
                ('delay', models.CharField(default=b'50000', max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('validate', models.CharField(default=b'0', max_length=1000)),
                ('robot', models.CharField(default=b'noview', max_length=1000)),
                ('mail_send', models.CharField(default=b'1', max_length=50)),
                ('segment', models.CharField(default=b'nosegment', max_length=50)),
                ('gr', models.CharField(default=b'2', max_length=50)),
                ('link', models.CharField(default=b'potenciales', max_length=1000)),
            ],
        ),
    ]
