import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MAIL_ADDRESS = os.getenv('MAIL_ADDRESS')
PASSWORD = os.getenv('PASSWORD')
HOME_URL = os.getenv('HOME_URL')
LOGIN_URL = os.getenv('LOGIN_URL')
DISCOUNT_URL = os.getenv('DISCOUNT_URL')
XPATH_AFTER_DISCOUNT_PRICE = os.getenv('XPATH_AFTER_DISCOUNT_PRICE')
XPATH_BEFORE_DISCOUNT_PRICE = os.getenv('XPATH_BEFORE_DISCOUNT_PRICE')
XPATH_DISCOUNT_RATIO = os.getenv('XPATH_DISCOUNT_RATIO')
XPATH_TAG_1 = os.getenv('XPATH_TAG_1')
XPATH_TAG_2 = os.getenv('XPATH_TAG_2')
XPATH_TAG_3 = os.getenv('XPATH_TAG_3')
XPATH_TAG_4 = os.getenv('XPATH_TAG_4')
XPATH_TAG_5 = os.getenv('XPATH_TAG_5')
XPATH_AFFILIATE_LINK = os.getenv('XPATH_AFFILIATE_LINK')
TWEET_HEADER = os.getenv('TWEET_HEADER')
XPATH_ACCOUNT = os.getenv('XPATH_ACCOUNT')
XPATH_LOGOUT = os.getenv('XPATH_LOGOUT')
SEARCH_WORD = os.getenv('SEARCH_WORD')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')