# -*- coding: utf-8 -*-
"""
mirrorresolv command

Poll all mirror URLs and determine whether they have IPv4 and/or IPv6 addresses
available.

Usage: ./manage.py mirrorresolv
"""

import sys
import logging

from django.core.management.base import BaseCommand
from mirrors.models import MirrorRsync

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s -> %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stderr)
logger = logging.getLogger()

class Command(BaseCommand):
    help = "Runs a check on all active mirror URLs to determine if they are reachable via IPv4 and/or v6."

    def handle(self, **options):
        v = int(options.get('verbosity', 0))
        if v == 0:
            logger.level = logging.ERROR
        elif v == 1:
            logger.level = logging.WARNING
        elif v >= 2:
            logger.level = logging.DEBUG

        return generate_rsync()


def generate_rsync():
    mirrors = MirrorRsync.objects.filter(mirror__tier=1).values('ip',
            'mirror__rsync_user', 'mirror__rsync_password')

    ips = [str(mirror['ip']) for mirror in mirrors]
    print(ips)


    with open('/tmp/rsyncd.secrets', 'w') as f:
        for mirror in mirrors:
            if mirror['mirror__rsync_user'] == '':
                continue
            f.write('{}:{}\n'.format(mirror['mirror__rsync_user'], mirror['mirror__rsync_password']))
