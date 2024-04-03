import boto3
import time, urllib
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):

    target_bucket = 'ctsdemo-output-data'    
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote(event['Records'][0]['s3']['object']['key'])
    copy_source = {'Bucket': source_bucket, 'Key': object_key}
    
    try:
        print ("Using waiter to waiting for object to persist through s3 service")
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket=source_bucket, Key=object_key)
        
        # copy the object to target S3
        s3.copy_object(Bucket=target_bucket, Key=object_key, CopySource=copy_source)
        
        # It will delete the objects/data from S3 bucket as soon as trigger/ event is invoked
        s3.delete_object(Bucket=source_bucket, Key=object_key)
        
        response = s3.head_object(Bucket=source_bucket, Key=object_key)
        
        print("CONTENT TYPE : "+str(response['ContentType']))
        print('Content-Length :'+str(response['ContentLength']))
        print('KeyName :'+str(object_key))
        print('Deleting object :'+str(object_key))       
        
        return response['ContentType']
        
    except Exception as err:
        print ("Error -"+str(err))
        return err
