import json
import boto3
from urllib.parse import urlparse, unquote_plus

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extract Transcribe job details from event
        transcription_job = event.get("TranscriptionJob", {})
        transcript_uri = transcription_job.get("Transcript", {}).get("TranscriptFileUri", "")

        if not transcript_uri:
            raise ValueError("Missing TranscriptFileUri in Transcribe job output")

        # Parse HTTPS URL (format: https://s3.region.amazonaws.com/bucket/key)
        parsed_uri = urlparse(transcript_uri)
        path = parsed_uri.path.lstrip('/')  # Remove leading slash

        # Split into [bucket, key] (e.g., "metadata-output-bucket1379/TranscribeJob-...")
        path_parts = path.split('/', 1)
        if len(path_parts) != 2:
            raise ValueError(f"Invalid S3 path: {path}")

        bucket = path_parts[0]
        key = unquote_plus(path_parts[1])

        # Debugging: Print parsed values
        print(f"Attempting to fetch from bucket: {bucket}, key: {key}")

        # Get transcript file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        transcript_data = json.loads(response['Body'].read().decode('utf-8'))

        # Extract pre-formatted transcript
        full_transcript = transcript_data['results']['transcripts'][0]['transcript']

        # Optional: Add speaker labels if needed
        speaker_labels = transcript_data.get('results', {}).get('speaker_labels', {})
        speaker_count = speaker_labels.get('speakers', 0)

        return {
            "callId": event.get("callId", "unknown"),
            "TranscriptText": full_transcript,
            "SpeakerCount": speaker_count,
            "WordCount": len(full_transcript.split()),
            "OriginalJob": transcription_job
        }

    except Exception as e:
        error_msg = f"Error processing transcript: {str(e)}"
        print(error_msg)
        return {
            "error": error_msg,
            "callId": event.get("callId", "unknown"),
            "TranscriptText": "",
            "Status": "FAILED"
        }