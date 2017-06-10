from testbase import ArchWebTestCase, TEST_USER, TEST_PASS, TEST_EMAIL

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class LoginTestCase(ArchWebTestCase):

    def setUp(self):
        ArchWebTestCase.setUp(self)

    def test_login(self):
        self.setup_user()
        self.open('/login')

        username = self.driver.find_element_by_id('id_username')
        username.send_keys(TEST_USER)
        password = self.driver.find_element_by_id('id_password')
        password.send_keys(TEST_PASS)
        password.send_keys(Keys.RETURN)

        element = self.driver.find_element_by_link_text('Logout')
        self.assertIsNotNone(element)


    def test_login_invalid(self):
        self.open('/login')

        username = self.driver.find_element_by_id('id_username')
        username.send_keys(TEST_USER)
        password = self.driver.find_element_by_id('id_password')
        password.send_keys(TEST_USER)
        password.send_keys(Keys.RETURN)

        with self.assertRaises(NoSuchElementException) as context:
                self.driver.find_element_by_link_text('Logout')
        self.assertTrue('no such element' in str(context.exception))
