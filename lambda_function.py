from selenium.common.exceptions import NoSuchElementException

import line
import twitter


def lambda_handler(event, context):
    for _ in range(3):
        try:
            twitter.login()
            twitter.tweet()
            twitter.logout()
        except (IndexError, NoSuchElementException):
            twitter.logout()
        except Exception as e:
            twitter.logout()
            line.send_line_notify(e)
        else:
            break
        finally:
            twitter.driver_quit()