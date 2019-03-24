"""
mirrornotify command

Notify's mirror administrator's of two types of mirror issues:
* "out of sync" if the lastsync time is older then 72 hours
* "unreachable"  if the lastsync file could not be fetched for 24 hours
"""


from django.core.management.base import BaseCommand

import sys
import logging

from mirrors.models import Mirror, MirrorUrl

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

        return notify_mirrors()

def notify_mirrors():
    logger.debug('requesting list of mirrors')
    for mirror in Mirror.objects.all():
        if not mirror.admin_email:
            logger.debug(f'Admin email not set for {mirror.name}')
            continue

        if not mirror.active:
            logger.debug(f'{mirror.name} is not active')
            continue

        for mirrorurl in MirrorUrl.objects.filter(mirror=mirror).all():
           print(mirrorurl)
