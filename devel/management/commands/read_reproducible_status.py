# -*- coding: utf-8 -*-
"""
read_reproducible_status command

Import reproducible status of packages.

Usage: ./manage.py read_reproducible_status <url>
"""

from collections import OrderedDict
from datetime import datetime
import logging
import subprocess
import sys

import requests

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from main.models import Arch, Repo, Package, RebuilderdStatus


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -> %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stderr)
logger = logging.getLogger()

# https://github.com/kpcyrd/rebuilderd/blob/master/common/src/lib.rs#L34
REBUILDERD_STATUSES = {
    'GOOD': 0,
    'BAD': 1,
    'UNKWN': 2,
}


class Command(BaseCommand):
    args = "<url>"
    help = "Import reproducible status from rebuilderd."

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*', help='<url>')

    def handle(self, *args, **options):
        v = int(options.get('verbosity', None))
        if v == 0:
            logger.level = logging.ERROR
        elif v == 1:
            logger.level = logging.INFO
        elif v >= 2:
            logger.level = logging.DEBUG

        if len(args) < 1:
            raise CommandError("rebuilderd url must be provided")

        import_rebuilderd_status(args[0])

def import_rebuilderd_status(url):
    statuses = []

    req = requests.get(url)
    data = req.json()

    for pkg in data:
        arch = Arch.objects.get(name=pkg['architecture'])
        repository = Repo.objects.get(name__iexact=pkg['suite'])

        pkgver, pkgrel = pkg['version'].rsplit('-', 1)

        dbpkg = Package.objects.filter(pkgname=pkg['name'], pkgver=pkgver,
                                    pkgrel=pkgrel, repo=repository, arch=arch)
        if not dbpkg:
            continue

        status = REBUILDERD_STATUSES.get(suite['status'], 2)
        rbstatus = RebuilderdStatus(pkg=pkg, status=status)
        statuses.append(rbstatus)

    RebuilderdStatus.objects.bulk_create(statuses)
