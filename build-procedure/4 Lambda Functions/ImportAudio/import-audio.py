import json
import boto3
import base64
from botocore.exceptions import ClientError

# Initialize the S3 client
s3_client = boto3.client('s3')

# Define the bucket name
BUCKET_NAME = 'input-audio-bucket1379'

def lambda_handler(event, context):
    print("Received event: ", json.dumps(event))  # Log the event to CloudWatch

    # Define common CORS headers
    cors_headers = {
        "Access-Control-Allow-Origin": "*",  # Change this to your specific domain if needed
        "Access-Control-Allow-Headers": "Content-Type,x-api-key",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"  # Include methods as needed
    }

    try:
        # Parse the body of the request (expected to be a JSON object)
        body = json.loads(event['body'])

        # Extract the file name, type, and base64-encoded file data
        file_name = body.get('fileName')
        file_type = body.get('fileType')
        file_data = body.get('fileData')  # base64-encoded data

        if not file_name or not file_data:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'message': 'Missing file name or file data.'})
            }

        # Decode the base64 file data
        file_content = base64.b64decode(file_data)

        # Upload the file to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content,
            ContentType=file_type
        )
        
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': f'File uploaded successfully: {file_name}'})
        }
        
    except ClientError as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'message': f"Failed to upload the file: {str(e)}"})
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({'message': f"Error processing the file: {str(e)}"})
        }
