import json

def lambda_handler(event, context):
    
    print( event['Records'][0]['Sns']['Subject'] )
    print( event['Records'][0]['Sns']['Message'] )
    print( event['Records'][0]['Sns']['Timestamp'] )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
