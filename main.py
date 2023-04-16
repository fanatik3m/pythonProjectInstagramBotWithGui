from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import pickle
import time
import os
from config import username, password


class InstagramBot:
    def __init__(self, _username: str, _password: str):
        self.user_name = _username
        self.password = _password

        self.url = 'https://www.instagram.com/'
        self.driver = webdriver.Chrome()

    def log_in(self):
        self.driver.get(url=self.url)
        time.sleep(5)

        if not os.path.exists(f'cookies/{self.user_name}_cookies'):
            print('[INFO] cookies dont exist')

            user_name_input = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input')
            user_name_input.send_keys(self.user_name)

            password_input = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input')
            password_input.send_keys(self.password)

            enter_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]')
            enter_button.click()

            time.sleep(5)

            pickle.dump(self.driver.get_cookies(), open(f'cookies/{self.user_name}_cookies', 'wb'))
        else:
            print('[INFO] cookies exist')

            for cookie in pickle.load(open(f'cookies/{self.user_name}_cookies', 'rb')):
                self.driver.add_cookie(cookie)

            time.sleep(3)
            self.driver.refresh()
            time.sleep(5)

            if self.check_xpath_exists('/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'):
                not_now_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
                not_now_button.click()

            time.sleep(3)

    def set_like(self, post_url):
        self.driver.get(url=post_url)
        time.sleep(5)

        like_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')

        if self.check_xpath_exists('/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button/div[2]'):
            like_button.click()
            print('[+] like set')
        else:
            print('[+] like already set')

        time.sleep(3)

    def check_xpath_exists(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def close(self):
        self.driver.close()
        self.driver.quit()


def main():
    bot = InstagramBot(username, password)

    bot.log_in()
    bot.set_like('[post_url]')


if __name__ == '__main__':
    main()

# :) :3