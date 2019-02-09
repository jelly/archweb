# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-17 20:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conflict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('version', models.CharField(default='', max_length=255)),
                ('comparison', models.CharField(default='', max_length=255)),
                ('pkg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conflicts', to='main.Package')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Depend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('version', models.CharField(default='', max_length=255)),
                ('comparison', models.CharField(default='', max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('deptype', models.CharField(choices=[('D', 'Depend'), ('O', 'Optional Depend'), ('M', 'Make Depend'), ('C', 'Check Depend')], default='D', max_length=1)),
                ('pkg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depends', to='main.Package')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FlagRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=254, verbose_name='email address')),
                ('created', models.DateTimeField(db_index=True, editable=False)),
                ('ip_address', models.GenericIPAddressField(unpack_ipv4=True, verbose_name='IP address')),
                ('pkgbase', models.CharField(db_index=True, max_length=255)),
                ('pkgver', models.CharField(max_length=255)),
                ('pkgrel', models.CharField(max_length=255)),
                ('epoch', models.PositiveIntegerField(default=0)),
                ('num_packages', models.PositiveIntegerField(default=1, verbose_name='number of packages')),
                ('message', models.TextField(blank=True, verbose_name='message to developer')),
                ('is_spam', models.BooleanField(default=False, help_text='Is this comment from a real person?')),
                ('is_legitimate', models.BooleanField(default=True, help_text='Is this actually an out-of-date flag request?')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Repo')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pkg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='main.Package')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='PackageGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('pkg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='main.Package')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='PackageRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pkgbase', models.CharField(max_length=255)),
                ('type', models.PositiveIntegerField(choices=[(1, 'Maintainer'), (2, 'Watcher')], default=1)),
                ('created', models.DateTimeField(editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_relations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Provision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('version', models.CharField(default='', max_length=255)),
                ('pkg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provides', to='main.Package')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Replacement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('version', models.CharField(default='', max_length=255)),
                ('comparison', models.CharField(default='', max_length=255)),
                ('pkg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replaces', to='main.Package')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Signoff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pkgbase', models.CharField(db_index=True, max_length=255)),
                ('pkgver', models.CharField(max_length=255)),
                ('pkgrel', models.CharField(max_length=255)),
                ('epoch', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(db_index=True, editable=False)),
                ('revoked', models.DateTimeField(null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('arch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Arch')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Repo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_signoffs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SignoffSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pkgbase', models.CharField(db_index=True, max_length=255)),
                ('pkgver', models.CharField(max_length=255)),
                ('pkgrel', models.CharField(max_length=255)),
                ('epoch', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(editable=False)),
                ('required', models.PositiveIntegerField(default=2, help_text='How many signoffs are required for this package?')),
                ('enabled', models.BooleanField(default=True, help_text='Is this package eligible for signoffs?')),
                ('known_bad', models.BooleanField(default=False, help_text='Is this package known to be broken in some way?')),
                ('comments', models.TextField(blank=True, null=True)),
                ('arch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Arch')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Repo')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pkgname', models.CharField(db_index=True, max_length=255)),
                ('pkgbase', models.CharField(max_length=255)),
                ('action_flag', models.PositiveSmallIntegerField(choices=[(1, 'Addition'), (2, 'Change'), (3, 'Deletion')], verbose_name='action flag')),
                ('created', models.DateTimeField(db_index=True, editable=False)),
                ('old_pkgver', models.CharField(max_length=255, null=True)),
                ('old_pkgrel', models.CharField(max_length=255, null=True)),
                ('old_epoch', models.PositiveIntegerField(null=True)),
                ('new_pkgver', models.CharField(max_length=255, null=True)),
                ('new_pkgrel', models.CharField(max_length=255, null=True)),
                ('new_epoch', models.PositiveIntegerField(null=True)),
                ('arch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='main.Arch')),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updates', to='main.Package')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='main.Repo')),
            ],
            options={
                'get_latest_by': 'created',
            },
        ),
        migrations.AlterUniqueTogether(
            name='packagerelation',
            unique_together=set([('pkgbase', 'user', 'type')]),
        ),
    ]