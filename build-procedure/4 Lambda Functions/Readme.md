# Lambda Functions Overview

## 1. ProcessUploadAudio Lambda

Purpose: Triggered when audio files are uploaded to input-audio-bucket1379; starts the Step Functions workflow.

Settings
- Runtime: Python 3.12

- Handler: lambda_function.lambda_handler

- IAM Role: PCA-Lambda-Role

- Timeout: 3 minutes (adjust if processing large files)

- Memory: 128 MB (default)

- Environment Variables (Optional):

    - STATE_MACHINE_ARN: ARN of your Step Functions workflow.

Trigger
- Source: S3 (input-audio-bucket1379)

- Event Type: s3:ObjectCreated:*

## 2. SyncToDynamoDB Lambda

Purpose: Triggered when JSON files are created in metadata-output-bucket1379; syncs metadata to DynamoDB.

Settings
- Runtime: Python 3.12

- Handler: dynamodb-sync.lambda_handler

- AM Role: PCA-Lambda-Role

- Timeout: 1 minute

- Memory: 128 MB

- Environment Variables (Optional):

    - DYNAMODB_TABLE: CallAnalytics

Trigger
- Source: S3 (metadata-output-bucket1379)

- Event Type: s3:ObjectCreated:*

## 3. DeleteFromDynamoDB Lambda

Purpose: Triggered when files are deleted from metadata-output-bucket1379; removes corresponding entries from DynamoDB.

Settings
- Runtime: Python 3.12

- Handler: dynamodb-delete.lambda_handler

- IAM Role: PCA-Lambda-Role

- Timeout: 1 minute

- Memory: 128 MB

Trigger
- Source: S3 (metadata-output-bucket1379)

- Event Type: s3:ObjectRemoved:*