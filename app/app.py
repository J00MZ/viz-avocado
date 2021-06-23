import urllib.parse
import boto3
from botocore.exceptions import ClientError

def send_file_email(bucket, filename, filetype):
    SENDER = "jtavin@gmail.com"
    RECIPIENT = "yosef.tavin@equalum.io"
    SUBJECT = f"File [{filename}] uploaded to {bucket}"
    BODY_TEXT = (f"File: {filename}"
                 f"File Type: {filetype}")
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>New File Uploaded to Bucket {bucket}</h1>
    <p>File: {filename}</br>
       File Type: {filetype}</br>
       Download file from: <a href='s3://{bucket}/{filename}'>Amazon S3</a>
    </p>
    </body>
    </html>
                """
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
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def handler(event, context):

    s3 = boto3.client('s3')
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        filetype = response['ContentType']
        print(f"FILE TYPE: {filetype}")
        print(f"FULL RESPONSE: {response}")
        send_file_email(bucket, key, filetype)
        return response['ContentType']
    except Exception as e:
        print(e)
        print(f'Error getting object {key} from bucket {bucket}. Make sure both exist and bucket is in same region as this function.')
        raise e
