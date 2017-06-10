from django.core.management import call_command
from django.contrib.auth.models import User, Group
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


TEST_USER = 'user1'
TEST_PASS = 'pass'
TEST_EMAIL = 'user1@archlinux.org'


class ArchWebTestCase(LiveServerTestCase):

    def setUp(self, login=False):
        self.driver = webdriver.Chrome()
        if login:
            self.login_user()
        print(Group.objects.all())

    def tearDown(self):
        self.driver.quit()

    def open(self, url):
        '''
        Open an url on archweb, example '/login'
        '''

        self.driver.get("{}{}".format(self.live_server_url, url))

    def setup_user(self):
        '''
        Create a test user
        '''

        # XXX: create_user does not work..
        self.user = User.objects.create_superuser(username=TEST_USER,
                                        last_name=TEST_USER,
                                        password=TEST_PASS,
                                        email=TEST_EMAIL)
        #self.user.groups.set_group(dev)

    def login_user(self):
        '''
        Login to Archweb
        '''

        self.setup_user()
        self.open('/login')

        username = self.driver.find_element_by_id('id_username')
        username.send_keys(TEST_USER)
        password = self.driver.find_element_by_id('id_password')
        password.send_keys(TEST_USER)
        password.send_keys(Keys.RETURN)
