
import json
import urllib.parse
import boto3
import requests

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        message = "EITA!!!! :eyes:\n Foi feito upload do arquivo {} com {} bytes".format(key, response['ContentLength'])
        data = {
            'channel':'#lambda-example',
            'icon_emoji': ':cloud:',
            'text': message,
            'username': 'Lambda-Bot'
        }
        print(message)
        r = requests.post(
            "WEBHOOK_TO_SLACK", # Define the webhook
            data = json.dumps(data)
        )
        print(r.text)
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
