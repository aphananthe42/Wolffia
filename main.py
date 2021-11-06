import datetime
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import tweepy


load_dotenv()
MAIL_ADDRESS = os.environ['MAIL_ADDRESS']
PASSWORD = os.environ['PASSWORD']
HOME_URL = os.environ['HOME_URL']
LOGIN_URL = os.environ['LOGIN_URL']
RANKING_URL = os.environ['RANKING_URL']
XPATH_3RD = os.environ['XPATH_3RD']
XPATH_2ND = os.environ['XPATH_2ND']
XPATH_1ST = os.environ['XPATH_1ST']
XPATH_COPY = os.environ['XPATH_COPY']
XPATH_ACCOUNT = os.environ['XPATH_ACCOUNT']
XPATH_LOGOUT = os.environ['XPATH_LOGOUT']
MSGK_WORDS_3RD = os.environ['MSGK_WORDS_3RD']
MSGK_WORDS_2ND = os.environ['MSGK_WORDS_2ND']
MSGK_WORDS_1ST = os.environ['MSGK_WORDS_1ST']
SEARCH_WORD = os.environ['SEARCH_WORD']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

path = '/usr/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=path, options=options)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def main():
    login()
    tweet()
    logout()
    follow()
    
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
    driver.get(RANKING_URL)
    if len(driver.find_elements_by_class_name('btn-approval')) > 0:
        approval_button = driver.find_element_by_class_name('btn-approval')
        approval_button.click()

    for i in range(3):
        if i == 0:
            ranking_element = driver.find_element_by_xpath(XPATH_3RD)
        elif i == 1:
            driver.get(RANKING_URL)
            ranking_element = driver.find_element_by_xpath(XPATH_2ND)
        elif i == 2:
            driver.get(RANKING_URL)
            ranking_element = driver.find_element_by_xpath(XPATH_1ST)
        ranking_element.click()

        affiliate_button = driver.find_element_by_class_name('guide_list')
        affiliate_button.click()

        if driver.current_url == HOME_URL:
            driver.back()
            affiliate_button = driver.find_element_by_class_name('guide_list')
            affiliate_button.click()

        copy_ref = driver.find_element_by_xpath(XPATH_COPY)
        affiliate_link = copy_ref.get_attribute('href')
        
        if i == 0:
            stamp = datetime.datetime.now()
            text = [MSGK_WORDS_3RD, stamp.strftime('[%Y/%m/%d %H:%M:%S]'), affiliate_link]
        elif i == 1:
            text = [MSGK_WORDS_2ND, stamp.strftime('[%Y/%m/%d %H:%M:%S]'), affiliate_link]
        elif i == 2:
            text = [MSGK_WORDS_1ST, stamp.strftime('[%Y/%m/%d %H:%M:%S]'), affiliate_link]
        tweet_content = '\n'.join(text)
        api.update_status(tweet_content)

def logout():
        driver_action = ActionChains(driver)
        account_menu = driver.find_element_by_xpath(XPATH_ACCOUNT)
        driver_action.move_to_element(account_menu).perform()
        logout_button = driver.find_element_by_xpath(XPATH_LOGOUT)
        logout_button.click()
        driver.quit()

def follow():
    query = SEARCH_WORD
    results = api.search_tweets(q=query, count=5)
    for result in results:
        screen_name = result.user.screen_name
        for _ in range(3):
            try:
                api.create_friendship(screen_name=screen_name)
            except tweepy.TooManyRequests:
                time.sleep(15 * 60)
            except tweepy.TweepyException:
                break
            else:
                time.sleep(5)
                break

if __name__ == '__main__':
    main()