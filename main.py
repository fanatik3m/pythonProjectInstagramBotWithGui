from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import pickle
import time
import os
from multiprocessing import Pool
from config import username, password


def ask_multiprocessing() -> bool:
    return bool(input('0 - without multiprocessing, 1 - with it: '))


def check_xpath_exists(xpath: str, driver):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except NoSuchElementException:
        return False


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

            if check_xpath_exists('/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]', self.driver):
                not_now_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
                not_now_button.click()

            time.sleep(3)

    def set_like(self, post_url):
        self.driver.get(url=post_url)
        time.sleep(5)

        like_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')

        if check_xpath_exists('/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button/div[2]', self.driver):
            like_button.click()
            print('[+] like set')
        else:
            print('[+] like already set')

        time.sleep(3)

    def close(self):
        self.driver.close()
        self.driver.quit()


def log_in(post_url: str):
    driver = webdriver.Chrome()
    driver.get('https://www.instagram.com/')
    time.sleep(5)

    for cookie in pickle.load(open(f'cookies/{username}_cookies', 'rb')):
        driver.add_cookie(cookie)

    print('[INFO] cookies loaded')
    time.sleep(3)
    driver.refresh()
    time.sleep(5)

    driver.get(url=post_url)
    time.sleep(5)

    like_button = driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')
    if check_xpath_exists(
            '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button/div[2]',
            driver):
        like_button.click()
        print('[+] like set')
    else:
        print('[+] like already set')

    time.sleep(3)


if __name__ == '__main__':
    posts = (
        'https://www.instagram.com/p/CrANRK9rni4/',
        'https://www.instagram.com/p/Cq-W4v4tjxx/',
        'https://www.instagram.com/p/Cq-3Sq3IhRE/'
    )

    if ask_multiprocessing():
        with Pool(os.cpu_count()) as pool:
            pool.map(log_in, posts)
    else:
        bot = InstagramBot(username, password)
        bot.log_in()
