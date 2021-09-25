#!/usr/bin/python3

import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options


krotida_root_url = 'https://drive.google.com/drive/u/0/folders/1KPrinUxLgQS5VBFR8nD-GnJymOVHFgNp'

input_email_field_selector1 = '#identifierId'
input_email_field_xpath1 = '//*[@id="identifierId"]'
input_email_field_xpath2 = '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/content/section/div/content/div[1]/div/div[1]/div/div[1]/div'
first_next_button_xpath = '//*[@id="identifierNext"]/content/span'
second_next_button_xpath = '//*[@id="passwordNext"]/content'


my_gmail_address = 'boromir674@gmail.com'


class KrotidaDoer:
    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # self.options = webdriver.ChromeOptions()

        # self.driver = webdriver.Chrome(chrome_options=self.options)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1024,800')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("user-data-dir=/home/kostas/.config/google-chrome/selenium_profile")  # Path to your chrome profile
        self.driver = webdriver.Chrome(chrome_options=chrome_options)



        sys.stderr.write(self.driver.title)

        # self.driver = webdriver.Chrome(chrome_options=self.options)
        # field in the first login screen prompting to input user email
        self._user_email_field = None
        # button to click after inputing user email
        self._next_button_1 = None
        # button to click after inputing user password
        self._next_button_2 = None

    def open_krotida_root_drive(self):
        """Opens in a new window the 'krotida-dir' google drive directory"""
        self.driver.get(krotida_root_url)

    def write_in_email_field(self, email):
        """Writes the given string in the 'user email' field of the google (ie gmail) login screen"""
        self._user_email_field = self.driver.find_element_by_xpath(input_email_field_xpath1)
        self._user_email_field.send_keys(email)
    
    def press_next_button(self, button_xpath):
        self._next_button_1 = self.driver.find_element_by_xpath(button_xpath)
        self._next_button_1.click()

    @staticmethod
    def _get_expected_condition(implemented_condition, xpath):
        return getattr(EC, implemented_condition)((By.XPATH, xpath))

    def _wait(self, seconds):
        return WebDriverWait(self.driver, seconds)

    def _get_item_on_condition(self, xpath, condition, seconds=2):
        """Call this method to get an element by xpath when the selected condition is satisfied.
        If the condiion is not satisfied within the given time interval it throws a TimeoutException"""
        return WebDriverWait(self.driver, seconds).until(KrotidaDoer._get_expected_condition(condition, xpath))

    def __call__(self):
        self.open_krotida_root_drive()

        # self.write_in_email_field(my_gmail_address)
        # pass
        # self.write_in_email_field(my_gmail_address)
        # self._next_button_1 = self.driver.find_element_by_xpath(first_next_button_xpath)
        # self._next_button_1.click()



if __name__ == '__main__':
    krotida_root_doer = KrotidaDoer()
    try:
        krotida_root_doer()
    except RuntimeError as e:
        print(e)
