import boto3

import settings


CELTIS_ACCESS_KEY_ID = settings.CELTIS_ACCESS_KEY_ID
CELTIS_SECRET_ACCESS_KEY = settings.CELTIS_SECRET_ACCESS_KEY
SNS_TOPIC_ARN = settings.SNS_TOPIC_ARN
region = 'ap-northeast-1'

sns = boto3.client(
    'sns', 
    aws_access_key_id=CELTIS_ACCESS_KEY_ID, 
    aws_secret_access_key=CELTIS_SECRET_ACCESS_KEY, 
    region_name=region
    )

def send(error):
    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=error
        )