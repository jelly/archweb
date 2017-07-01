# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.db import migrations, models


def initialize_data(apps, schema_editor):
    arches = json.load(open('main/fixtures/arches.json'))
    groups = json.load(open('main/fixtures/groups.json'))
    repos = json.load(open('main/fixtures/repos.json'))

    for record in arches + repos:
        app_name, model_name = record['model'].split('.')
        ModelClass = apps.get_model(app_name, model_name)
        obj = ModelClass(**record['fields'])
        obj.save


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_data)
    ]
