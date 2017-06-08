from django.test import LiveServerTestCase
from selenium import webdriver


TEST_USER = 'user1'
TEST_PASS = 'pass'
TEST_EMAIL = 'user1@archlinux.org'


class ArchWebTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def open(self, url):
        '''
        Open an url on archweb, example '/login'
        '''

        self.driver.get("{}{}".format(self.live_server_url, url))
