import json
import boto3
import uuid
import hashlib  # Added missing import

def lambda_handler(event, context):
    try:
        print("Raw event:", json.dumps(event))  # Debugging
        
        # Validate event structure
        if not event.get('Records') or not event['Records'][0].get('s3'):
            raise ValueError("Invalid S3 event format")
            
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f"Processing: s3://{bucket}/{key}")

        # Generate a unique callId (UUID4)
        call_id = str(uuid.uuid4())
        print(f"Generated callId: {call_id}")

        stepfunctions = boto3.client('stepfunctions')
        
        # Create execution ID with callId + MD5 hash of bucket/key
        execution_id = f"{call_id}-{hashlib.md5(f'{bucket}/{key}'.encode()).hexdigest()}"
        print(f"Generated execution ID: {execution_id}")

        try:
            # Check for duplicate executions (prevents reprocessing)
            stepfunctions.describe_execution(
                executionArn=f"arn:aws:states:us-east-1:593793068175:execution:MyStateMachine-s2t060l08:{execution_id}"
            )
            print(f"Duplicate execution detected: {execution_id}")
            return {
                "statusCode": 200,
                "body": json.dumps({"status": "skipped", "reason": "Duplicate execution"})
            }

        except stepfunctions.exceptions.ExecutionDoesNotExist:
            # Start new execution with callId payload
            response = stepfunctions.start_execution(
                stateMachineArn='arn:aws:states:us-east-1:593793068175:stateMachine:MyStateMachine-s2t060l08',
                name=execution_id,
                input=json.dumps({
                    'callId': call_id,
                    'bucket': bucket,
                    'key': key
                })
            )
            print(f"Started execution: {response['executionArn']}")
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": "started",
                    "callId": call_id,
                    "executionArn": response['executionArn']
                })
            }

        except Exception as e:
            print(f"Step Functions API Error: {str(e)}")
            raise

    except Exception as e:
        print(f"Fatal Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "message": "Failed to process audio upload"
            })
        }