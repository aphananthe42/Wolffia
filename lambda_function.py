import sns
import twitter


def lambda_handler(event, context):
    twitter.login()
    for i in range(3):
        try:
            twitter.tweet()
        except Exception as error:
            if i == 2:
                sns.send(error)
        else:
            twitter.logout()
            twitter.driver_quit()
            break