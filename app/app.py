import sys
import boto3

def handler(event, context):

    s3 = boto3.resource('s3')
    object_summary = s3.ObjectSummary('avocado-file-toaster','test-file')
    response = object_summary.get(
                ResponseContentType='string'
            )
    return 'Hello from AWS Lambda using Python' + sys.version + '!' + response
