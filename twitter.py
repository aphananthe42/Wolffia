import datetime
import random

from selenium.webdriver.chrome.webdriver import WebDriver
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
GUIDE_URL = settings.GUIDE_URL
XPATH_AFTER_DISCOUNT_PRICE = settings.XPATH_AFTER_DISCOUNT_PRICE
XPATH_BEFORE_DISCOUNT_PRICE = settings.XPATH_BEFORE_DISCOUNT_PRICE
XPATH_AFFILIATE_LINK = settings.XPATH_AFFILIATE_LINK
TWEET_HEADER = settings.TWEET_HEADER
XPATH_ACCOUNT = settings.XPATH_ACCOUNT
XPATH_LOGOUT = settings.XPATH_LOGOUT
SEARCH_WORD = settings.SEARCH_WORD
CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN_KEY = settings.ACCESS_TOKEN_KEY
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET
LINE_NOTIFY_API_URL = settings.LINE_NOTIFY_API_URL
LINE_NOTIFY_TOKEN = settings.LINE_NOTIFY_TOKEN

path = '/opt/headless/python/bin/chromedriver'
options = Options()
options.binary_location = '/opt/headless/python/bin/headless-chromium'
options.add_argument('start-maximized')
options.add_argument('enable-automation')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')
options.add_argument("--single-process")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
prefs = {'profile.default_content_setting_values.notifications': 2}
options.add_experimental_option('prefs', prefs)
driver = WebDriver(executable_path=path, options=options)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def login():
    driver.get(LOGIN_URL)

    id = driver.find_element_by_id('form_id')
    id.clear()
    id.send_keys(MAIL_ADDRESS)

    password = driver.find_element_by_id('form_password')
    password.clear()
    password.send_keys(PASSWORD)

    login_button = driver.find_element_by_class_name('loginBtn')
    login_button.click()

def tweet():
    driver.get(DISCOUNT_URL)
    if len(driver.find_elements_by_class_name('btn-approval')) > 0:
        approval_button = driver.find_element_by_class_name('btn-approval')
        approval_button.click()

    random_number = random.randint(1, 100)
    xpath_content = f'//*[@id="search_result_img_box"]/li[{random_number}]/dl/dd[2]/div[2]/a'
    content_url = driver.find_element_by_xpath(xpath_content).get_attribute('href')
    driver.get(content_url)
    
    guide_url = driver.find_element_by_xpath(GUIDE_URL).get_attribute('href')
    driver.get(guide_url)

    discount_ratio = driver.find_element_by_class_name('icon_campaign').text
    before_discount_price = driver.find_element_by_xpath(XPATH_BEFORE_DISCOUNT_PRICE).text
    after_discount_price = driver.find_element_by_xpath(XPATH_AFTER_DISCOUNT_PRICE).text
    search_tag = driver.find_element_by_class_name('search_tag')
    tags = search_tag.find_elements_by_tag_name('a')
    tag1 = tags[0].text
    tag2 = tags[1].text
    tag3 = tags[2].text
    tag4 = tags[3].text
    tag5 = tags[4].text
    affiliate_link = driver.find_element_by_xpath(XPATH_AFFILIATE_LINK).get_attribute('href')
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
    account_menu = driver.find_element_by_xpath(XPATH_ACCOUNT)
    driver_action.move_to_element(account_menu).perform()
    logout_button = driver.find_element_by_xpath(XPATH_LOGOUT)
    logout_button.click()
    driver.quit()
        
def driver_quit():
    driver.quit()
    