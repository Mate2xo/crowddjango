from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginFeatureTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_login_with_valid_params(self):
        User.objects.create_user(username='marcodu93', password='passpass')

        self.browser.get(f'{self.live_server_url}/accounts/login/')
        self.browser.find_element(By.ID, 'id_username').send_keys('marcodu93')
        self.browser.find_element(By.ID, 'id_password').send_keys('passpass')
        self.browser.find_element(By.ID, 'id_submit').click()

        self.assertIn('/accounts/profile', self.browser.current_url)
