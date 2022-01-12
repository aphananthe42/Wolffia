import line
import twitter


def lambda_handler(event, context):
    twitter.login()
    for i in range(3):
        try:
            twitter.tweet()
        except Exception as e:
            if i == 2:
                line.send_line_notify(e)
        else:
            twitter.logout()
            twitter.driver_quit()
            break