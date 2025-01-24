import json
import boto3
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CallAnalytics')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            key = unquote_plus(record['s3']['object']['key'])
            
            # Extract CallId from the S3 key (customize based on your naming convention)
            call_id = key.split('/')[-1].replace('.json', '')
            
            # Delete from DynamoDB
            table.delete_item(Key={'CallId': call_id})
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise