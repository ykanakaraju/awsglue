import json

def lambda_handler(event, context):
    
    print ("running the python function")
    
    print( event['key1'] )
    print( event['key2'] )
    print( event['key3'] )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



