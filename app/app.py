import urllib.parse
import boto3
import os
from botocore.exceptions import ClientError

def send_file_email(bucket, filename, filetype):
    SENDER = os.environ['EMAIL_SENDER']
    RECIPIENT = os.environ['EMAIL_RECIEVER']
    SUBJECT = f"File [{filename}] uploaded to {bucket}"
    BODY_TEXT = (f"File: {filename}"
                 f"File Type: {filetype}")
    BODY_HTML = f"""
    <html>
        <head></head>
        <body>
            <p>File: {filename}</p>
            <p>File Type: {filetype}</p>
            <p>File S3 URI: s3://{bucket}/{filename}</p>
        </body>
    </html>"""
    CHARSET = "UTF-8"

    client = boto3.client('ses')

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent!"),
        print(f"Message ID: {response['MessageId']}")

def handler(event, context):

    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        filetype = response['ContentType']
        print(f"FILE TYPE: {filetype}")
        send_file_email(bucket, key, filetype)
        return filetype
    except Exception as e:
        print(e)
        print(f'Error getting object {key} from bucket {bucket}. Make sure both exist and bucket is in same region as this function.')
        raise e

