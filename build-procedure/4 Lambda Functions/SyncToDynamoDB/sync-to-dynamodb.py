import json
import boto3
from urllib.parse import unquote_plus

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CallAnalytics')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            
            # Fetch JSON from S3
            response = s3.get_object(Bucket=bucket, Key=key)
            data = json.loads(response['Body'].read().decode('utf-8'))
            
            # Extract metadata (customize based on JSON schema)
            table.put_item(Item={
                'CallId': data['CallId'],
                'Timestamp': data['Timestamp'],
                'Sentiment': data['Sentiment'],
                'S3Location': f"s3://{bucket}/{key}",
                'Duration': data.get('Duration', 0),
                'AgentId': data.get('AgentId', 'unknown')
            })
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise