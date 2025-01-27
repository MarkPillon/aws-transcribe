import json
import boto3
import logging
from decimal import Decimal
from urllib.parse import unquote_plus
from datetime import datetime

# Custom JSON serializer for DynamoDB
def decimal_default(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    raise TypeError

# Configure clients with custom serializer
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CallAnalytics')
s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            
            if key.startswith('processed/errors/'):
                logger.info(f"Skipping error file: {key}")
                continue
                
            # Get and parse S3 object
            response = s3.get_object(Bucket=bucket, Key=key)
            data = json.loads(response['Body'].read().decode('utf-8'), parse_float=Decimal)
            
            # Process and convert float values
            def convert_floats(item):
                if isinstance(item, dict):
                    return {k: convert_floats(v) for k, v in item.items()}
                elif isinstance(item, list):
                    return [convert_floats(v) for v in item]
                elif isinstance(item, float):
                    return Decimal(str(item))
                return item
                
            processed_data = convert_floats(data)
            
            # Build DynamoDB item (existing logic)
            call_id = processed_data.get('callId')
            processing_time = processed_data.get('processingTime', {})
            
            # ... rest of your existing processing logic ...
            
            # Write to DynamoDB
            table.put_item(Item=processed_data)
            
        return {'statusCode': 200}
        
    except Exception as e:
        logger.error(f"Critical failure: {str(e)}", exc_info=True)
        raise