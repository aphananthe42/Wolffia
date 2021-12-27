import requests

import settings


LINE_NOTIFY_API_URL = settings.LINE_NOTIFY_API_URL
LINE_NOTIFY_TOKEN = settings.LINE_NOTIFY_TOKEN

def send_line_notify(error):
    headers = {
        'Authorization': 'Bearer' + ' ' + LINE_NOTIFY_TOKEN
    }
    data = {
        'message': error
    }
    requests.post(LINE_NOTIFY_API_URL, headers=headers, data=data)