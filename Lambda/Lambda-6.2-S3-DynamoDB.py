#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#table
#https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html     


import boto3
s3_client = boto3.client("s3")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_file_name = event['Records'][0]['s3']['object']['key']
    resp = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
    data = resp['Body'].read().decode("utf-8")
    #print(data)
    
    users = data.split("\n")
    
    for user in users:
        print(user)
        
        user_data = user.split(",")
        
        table.put_item(
            Item = {
                "id" : user_data[0],
                "name": user_data[1],
                "gender": user_data[2],
                "age": user_data[3],
                "mobile": user_data[4]
            }
        )