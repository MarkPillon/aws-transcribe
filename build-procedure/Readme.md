# Order of Creation

1. IAM Roles
    -  PCA-Lambda-Role (for Lambda functions)

    - PCA-StepFunctions-Role (for Step Functions)

    - PCA-WebApp-Upload-Role (optional, for web app uploads)

2. S3 Buckets
    - input-audio-bucket1379 (with policy allowing PCA-WebApp-Upload-Role to write)

    - metadata-output-bucket1379

3. DynamoDB Table
    - CallAnalytics (for metadata storage)

4. Lambda Functions
    - ProcessUploadAudio (triggered by input-audio-bucket1379)

    - SyncToDynamoDB (triggered by metadata-output-bucket1379 object creation)

    - DeleteFromDynamoDB (triggered by metadata-output-bucket1379 object deletion)

5. Step Functions Workflow
    - PostCallAnalyticsWorkflow (orchestrates Transcribe → Comprehend → S3 output)

6. Triggers
    - S3 → Lambda triggers for input/output buckets.

    - Web App configured to use PCA-WebApp-Upload-Role for secure uploads (optional).

### Key Notes
- Dependencies:

    - IAM roles must exist before S3 bucket policies reference them.

    - DynamoDB table must exist before SyncToDynamoDB Lambda runs.

    - Step Functions requires S3 buckets and Lambda functions to be operational.
