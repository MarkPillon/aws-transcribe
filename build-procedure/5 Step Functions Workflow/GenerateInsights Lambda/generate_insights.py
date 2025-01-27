import json
import boto3
import os
from botocore.exceptions import ClientError
from botocore.config import Config

bedrock_config = Config(
    retries={'max_attempts': 3, 'mode': 'standard'}
)
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1', config=bedrock_config)

def lambda_handler(event, context):
    call_id = event.get("callId", "unknown")  # Always extract callId first
    
    try:
        print("Received event:", json.dumps(event))
        
        # Validate inputs
        transcript = event.get("Transcript", "")
        sentiment = event.get("Sentiment", "NEUTRAL")
        
        if not transcript.strip():
            raise ValueError("Empty transcript received")

        # Bedrock API call
        prompt = f"""Human: Analyze call ID: {call_id}. Sentiment: {sentiment}.
        Provide 3 concise insights in bullet points. Focus on key issues and resolutions.
        Transcript: {transcript}
        Assistant:"""
        
        response = bedrock.invoke_model(
            modelId=os.getenv('BEDROCK_MODEL', 'anthropic.claude-instant-v1'),
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.3
            })
        )
        
        result = json.loads(response['body'].read().decode())
        insights = result['completion'].strip()
        
        return {
            "callId": call_id,
            "Insights": insights,
            "Model": os.getenv('BEDROCK_MODEL', 'anthropic.claude-instant-v1'),
            "Status": "SUCCESS"
        }
        
    except Exception as e:
        print(f"Error processing call {call_id}: {str(e)}")
        return {
            "callId": call_id,  # <-- Critical: Always include callId
            "error": str(e),
            "Insights": "Failed to generate insights",
            "Status": "ERROR"
        }