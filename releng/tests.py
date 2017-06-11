import hashlib
from datetime import datetime

from django.test import TestCase

from releng.models import Release


class RelengTest(TestCase):
    fixtures = ['releng/fixtures/release.json']

    def test_feed(self):
        response = self.client.get('/feeds/releases/')
        self.assertEqual(response.status_code, 200)

    def test_release(self):
        print(Release.objects.all())
