'''
You can use this script to prevent some file types to be uploaded to S3
When you add S3 trigger to the lambda specify a suffix like .py 
    -> This automatically deletes any python files from s3
You can add multiple trigger to add multiple suffixes
'''

import boto3
import time, urllib
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
    
    try:
        print ("Using waiter to waiting for object to persist through s3 service")
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket=bucket, Key=object_key)
        response = s3.head_object(Bucket=bucket, Key=object_key)
        print ("CONTENT TYPE : "+str(response['ContentType']))
        print ('ETag :' +str(response['ETag']))
        print ('Content-Length :'+str(response['ContentLength']))
        print ('KeyName :'+str(object_key))
        print ('Deleting object :'+str(object_key))
        # It will delete the objects/data from S3 bucket as soon as trigger/ event is invoked
        s3.delete_object(Bucket=bucket, Key=object_key)
        return response['ContentType']
    except Exception as err:
        print ("Error -"+str(err))
        return err
