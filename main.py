import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pickle
import time
import os
from multiprocessing import Pool
from config import username, password


def ask_multiprocessing() -> bool:
    return bool(int(input('0 - without multiprocessing, 1 - with it: ')))


class InstagramBot:
    def __init__(self, _username: str, _password: str):
        self.user_name = _username
        self.password = _password

        self.url = 'https://www.instagram.com/'
        self.driver = webdriver.Chrome()

    def log_in(self) -> None:
        self.driver.get(url=self.url)

        if not os.path.exists(f'cookies/{self.user_name}_cookies'):
            print('[INFO] cookies dont exist')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input')))

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

            # self.driver.refresh()

    def set_like(self, post_url: str) -> None:
        self.driver.get(url=post_url)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')))

        like_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button')

        if self.check_xpath_exists('/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button/div[2]'):
            like_button.click()
            print('[+] like set')
        else:
            print('[+] like already set')

    def check_xpath_exists(self, xpath: str) -> bool:
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def close(self) -> None:
        self.driver.close()
        self.driver.quit()


def log_in_set_likes(post_url: str) -> None:
    instagram_bot = InstagramBot(username, password)
    instagram_bot.log_in()
    instagram_bot.set_like(post_url)
    instagram_bot.close()


if __name__ == '__main__':
    posts = (
        'https://www.instagram.com/p/CrANRK9rni4/',
        'https://www.instagram.com/p/CrANRK9rni4/',
        'https://www.instagram.com/p/CrANRK9rni4/',
        'https://www.instagram.com/p/CrANRK9rni4/',
        'https://www.instagram.com/p/CrANRK9rni4/',
        'https://www.instagram.com/p/CrANRK9rni4/',
        'https://www.instagram.com/p/CrANRK9rni4/',
        'https://www.instagram.com/p/CrANRK9rni4/'
    )

    if len(posts) == 1:
        bot = InstagramBot(username, password)
        bot.log_in()
        bot.set_like(posts[0])
        bot.close()

    _multiprocessing = ask_multiprocessing()

    if _multiprocessing:
        start_time = datetime.datetime.now()
        with Pool(os.cpu_count()) as pool:
            pool.map(log_in_set_likes, posts)
        print(f'Total time is {datetime.datetime.now() - start_time}')
    else:
        start_time = datetime.datetime.now()
        bot = InstagramBot(username, password)
        bot.log_in()
        for url in posts:
            bot.set_like(url)
        bot.close()
        print(f'Total time is {datetime.datetime.now() - start_time}')
