from django.core.management import call_command
from django.contrib.auth.models import User, Group
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


TEST_USER = 'developer'
TEST_PASS = 'developer'
TEST_EMAIL = 'developer@archlinux.org'

TITLE = 'Dropping i686'
CONTENT = 'After many years we will finally drop i686!'

class NewsIntegrationTestCase(LiveServerTestCase):
    fixtures = ['main/fixtures/arches.json', 'main/fixtures/repos.json',
                'main/fixtures/users.json', 'main/fixtures/groups.json',
                'devel/fixtures/staff_groups.json', 'devel/fixtures/userprofile.json']


    @classmethod
    def setUpClass(self):
        super(NewsIntegrationTestCase, self).setUpClass()
        self.driver = webdriver.Chrome()

    def setUp(self):
        self.login_user()
        self.open('/news')

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(NewsIntegrationTestCase, self).tearDownClass()

    def open(self, url):
        '''
        Open an url on archweb, example '/login'
        '''

        self.driver.get("{}{}".format(self.live_server_url, url))

    def login_user(self):
        '''
        Login to Archweb
        '''

        self.open('/login')

        username = self.driver.find_element_by_id('id_username')
        username.send_keys(TEST_USER)
        password = self.driver.find_element_by_id('id_password')
        password.send_keys(TEST_USER)
        password.send_keys(Keys.RETURN)

        elem = self.driver.find_element_by_link_text('Logout')
        assert elem.text == 'Logout'

    def setupNews(self):
        self.driver.find_element_by_link_text('Add News Item').click()

        title_elem = self.driver.find_element_by_id('id_title')
        title_elem.send_keys(TITLE)

        content_elem = self.driver.find_element_by_id('id_content')
        content_elem.send_keys(CONTENT)

    def testPreview(self):
        self.setupNews()

        preview_elem = self.driver.find_element_by_id('news-preview-button')
        preview_elem.click()

        preview_title_elem = self.driver.find_element_by_id('news-preview-title')
        self.assertEquals(preview_title_elem.text, TITLE)

        preview_content_elem = self.driver.find_element_by_id('news-preview-data')
        self.assertEquals(preview_content_elem.text, CONTENT)

    def testCreate(self):
        self.setupNews()

        save_button = self.driver.find_element_by_id('news-save-button')
        save_button.click()

        title_elem = self.driver.find_element_by_tag_name('h2')
        self.assertEquals(title_elem.text, TITLE)

        content_elem = self.driver.find_element_by_class_name('article-content')
        self.assertEquals(content_elem.text, CONTENT)

        self.open('/news')
