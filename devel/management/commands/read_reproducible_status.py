# -*- coding: utf-8 -*-
"""
read_reproducible_status command

Import reproducible status of packages, rebuilderd url configured in django
settings.

Usage: ./manage.py read_reproducible_status
"""

import logging
import sys

import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from main.models import Arch, Repo, Package, RebuilderdStatus


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -> %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stderr)
logger = logging.getLogger()


class Command(BaseCommand):
    help = "Import reproducible status from rebuilderd."

    def handle(self, *args, **options):
        v = int(options.get('verbosity', None))
        if v == 0:
            logger.level = logging.ERROR
        elif v == 1:
            logger.level = logging.INFO
        elif v >= 2:
            logger.level = logging.DEBUG

        url = getattr(settings, "REBUILDERD_URL", None)
        if not url:
            logger.error("no rebuilderd_url configured in local_settings.py")

        import_rebuilderd_status(url)


def import_rebuilderd_status(url):
    statuses = []

    req = requests.get(url)
    data = req.json()

    for pkg in data:
        arch = Arch.objects.get(name=pkg['architecture'])
        repository = Repo.objects.get(name__iexact=pkg['suite'])

        pkgver, pkgrel = pkg['version'].rsplit('-', 1)

        dbpkg = Package.objects.filter(pkgname=pkg['name'], pkgver=pkgver,
                                       pkgrel=pkgrel, repo=repository,
                                       arch=arch).first()
        if not dbpkg:
            continue

        rebuilderdpkg = RebuilderdStatus.objects.filter(pkg=dbpkg)
        if rebuilderdpkg:
            continue

        logger.info('adding status for package: %s', pkg['name'])

        status = RebuilderdStatus.REBUILDERD_API_STATUSES.get(pkg['status'], RebuilderdStatus.UNKNOWN)
        rbstatus = RebuilderdStatus(pkg=dbpkg, status=status)
        statuses.append(rbstatus)

    RebuilderdStatus.objects.bulk_create(statuses)
