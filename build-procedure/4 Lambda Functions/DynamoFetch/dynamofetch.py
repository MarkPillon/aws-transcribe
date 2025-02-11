import json
import boto3
import logging
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def decimal_default(obj):
    """Convert Decimal types to float for JSON serialization"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    # Define CORS headers (update origin to your specific frontend URL if needed)
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Safely extract query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        call_id = query_params.get('callId')
        
        # Validate required parameter
        if not call_id:
            logger.error("Missing callId parameter")
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({"error": "Missing callId query parameter"})
            }

        logger.info(f"Searching for callId: {call_id}")
        
        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('CallAnalytics')
        
        # Get item from DynamoDB
        response = table.get_item(Key={'callId': call_id})
        logger.info(f"DynamoDB response: {json.dumps(response, default=decimal_default)}")
        
        # Handle missing item
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "headers": cors_headers,
                "body": json.dumps({"error": "Call ID not found"})
            }

        # Return successful response with Decimal handling
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps(response['Item'], default=decimal_default)
        }

    except ClientError as e:
        logger.error(f"DynamoDB Error: {e.response['Error']['Message']}")
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": "Database error"})
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": "Internal server error"})
        }