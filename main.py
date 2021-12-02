import datetime
import random

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import tweepy

import settings


MAIL_ADDRESS = settings.MAIL_ADDRESS
PASSWORD = settings.PASSWORD
HOME_URL = settings.HOME_URL
LOGIN_URL = settings.LOGIN_URL
DISCOUNT_URL = settings.DISCOUNT_URL
XPATH_DISCOUNT_RATIO = settings.XPATH_DISCOUNT_RATIO
XPATH_AFTER_DISCOUNT_PRICE = settings.XPATH_AFTER_DISCOUNT_PRICE
XPATH_BEFORE_DISCOUNT_PRICE = settings.XPATH_BEFORE_DISCOUNT_PRICE
XPATH_TAG_1 = settings.XPATH_TAG_1
XPATH_TAG_2 = settings.XPATH_TAG_2
XPATH_TAG_3 = settings.XPATH_TAG_3
XPATH_TAG_4 = settings.XPATH_TAG_4
XPATH_TAG_5 = settings.XPATH_TAG_5
XPATH_AFFILIATE_LINK = settings.XPATH_AFFILIATE_LINK
TWEET_HEADER = settings.TWEET_HEADER
XPATH_ACCOUNT = settings.XPATH_ACCOUNT
XPATH_LOGOUT = settings.XPATH_LOGOUT
SEARCH_WORD = settings.SEARCH_WORD
CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN_KEY = settings.ACCESS_TOKEN_KEY
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET

path = '/usr/bin/chromedriver'
service = Service(executable_path=path)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-setuid-sandbox')
driver = WebDriver(options=options, service=service)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def main():
    follow()
    login()
    tweet()
    logout()
    print('finished successfully.')
    print('----------------------')
    
def follow():
    query = SEARCH_WORD
    results = api.search_tweets(q=query, count=3)
    for result in results:
        screen_name = result.user.screen_name
        try:
            api.create_friendship(screen_name=screen_name)
        except Exception as e:
            print(e)

def login():
        driver.get(LOGIN_URL)

        id = driver.find_element(By.ID, 'form_id')
        id.clear()
        id.send_keys(MAIL_ADDRESS)

        password = driver.find_element(By.ID, 'form_password')
        password.clear()
        password.send_keys(PASSWORD)

        login_button = driver.find_element(By.CLASS_NAME, 'loginBtn')
        login_button.click()

def tweet():
    driver.get(DISCOUNT_URL)
    if len(driver.find_elements(By.CLASS_NAME, 'btn-approval')) > 0:
        approval_button = driver.find_element(By.CLASS_NAME, 'btn-approval')
        approval_button.click()

    random_number = random.randint(1, 100)
    xpath_content = f'//*[@id="search_result_img_box"]/li[{random_number}]/dl/dd[2]/div[2]/a'
    content_url = driver.find_element(By.XPATH, xpath_content).get_attribute('href')
    driver.get(content_url)

    affiliate_button = driver.find_element(By.CLASS_NAME, 'guide_list')
    affiliate_button.click()

    if driver.current_url == HOME_URL:
        driver.back()
        affiliate_button = driver.find_element(By.CLASS_NAME, 'guide_list')
        affiliate_button.click()

    discount_ratio = driver.find_element(By.XPATH, XPATH_DISCOUNT_RATIO).text
    before_discount_price = driver.find_element(By.XPATH, XPATH_BEFORE_DISCOUNT_PRICE).text
    after_discount_price = driver.find_element(By.XPATH, XPATH_AFTER_DISCOUNT_PRICE).text
    tag1 = driver.find_element(By.XPATH, XPATH_TAG_1).text
    tag2 = driver.find_element(By.XPATH, XPATH_TAG_2).text
    tag3 = driver.find_element(By.XPATH, XPATH_TAG_3).text
    tag4 = driver.find_element(By.XPATH, XPATH_TAG_4).text
    tag5 = driver.find_element(By.XPATH, XPATH_TAG_5).text
    affiliate_link = driver.find_element(By.XPATH, XPATH_AFFILIATE_LINK).get_attribute('href')
    stamp = datetime.datetime.now()

    text = [
        TWEET_HEADER,
        '【' + discount_ratio + '】',
        before_discount_price + ' ' + '➔➔➔' + ' ' + after_discount_price,
        ' #' + tag1 + ' #' + tag2 + ' #' + tag3,
        ' #' + tag4 + ' #' + tag5,
        stamp.strftime('[%Y/%m/%d %H:%M:%S]'),
        affiliate_link
    ]
    tweet_content = '\n'.join(text)
    api.update_status(tweet_content)

def logout():
        driver_action = ActionChains(driver)
        account_menu = driver.find_element(By.XPATH, XPATH_ACCOUNT)
        driver_action.move_to_element(account_menu).perform()
        logout_button = driver.find_element(By.XPATH, XPATH_LOGOUT)
        logout_button.click()
        driver.quit()

if __name__ == '__main__':
    main()