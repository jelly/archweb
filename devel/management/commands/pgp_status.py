from datetime import datetime, timedelta
import logging
import sys

from django.core.management.base import BaseCommand, CommandError
from devel.models import DeveloperKey, PGPSignature
from django.utils import timezone

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -> %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stderr)
logger = logging.getLogger()

class Command(BaseCommand):
    help = "Check if a key is almost expired or revoked."

    def handle(self, *args, **options):
        v = int(options.get('verbosity', None))
        if v == 0:
            logger.level = logging.ERROR
        elif v == 1:
            logger.level = logging.INFO
        elif v >= 2:
            logger.level = logging.DEBUG

        now = timezone.now()
        warning = now + timedelta(days=100)

        for key in DeveloperKey.objects.filter(expires__range=(now, warning)):
                print(key)
