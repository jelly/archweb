from django.test import TestCase

from mirrors.tests import create_mirror_url, delete_all_mirror_urls


class MirrorTest(TestCase):

    def tearDown(self):
        delete_all_mirror_urls()

    def test_details(self):
        response = self.client.get('/mirrors/nothing/')
        self.assertEqual(response.status_code, 404)

        mirror_url = create_mirror_url()
        url = mirror_url.mirror.get_absolute_url()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # FIXME: request as mirror admin

    def test_details_json(self):
        response = self.client.get('/mirrors/nothing/json/')
        self.assertEqual(response.status_code, 404)

        mirror_url = create_mirror_url()
        url = mirror_url.mirror.get_absolute_url()

        response = self.client.get(url + 'json/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotEqual(data['urls'], [])

    def test_url_details(self):
        mirror_url = create_mirror_url()
        url = mirror_url.mirror.get_absolute_url()

        response = self.client.get(url + '{}/'.format(mirror_url.id))
        self.assertEqual(response.status_code, 200)
