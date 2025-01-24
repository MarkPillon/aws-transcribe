import json
import boto3

def lambda_handler(event, context):
    stepfunctions = boto3.client('stepfunctions')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Start Step Functions workflow
    response = stepfunctions.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine/PostCallAnalyticsWorkflow',
        input=json.dumps({'bucket': bucket, 'key': key})
    )
    return response