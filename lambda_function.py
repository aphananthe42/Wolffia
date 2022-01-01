from selenium.common.exceptions import NoSuchElementException

import line
import twitter


def lambda_handler(event, context):
    try:
        twitter.login()
        twitter.tweet()
        twitter.logout()
    except NoSuchElementException:
        twitter.tweet()
        twitter.logout()
    except Exception as e:
        line.send_line_notify(e)
    finally:
        twitter.driver_quit()