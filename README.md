# Building Post-Call Analytics on AWS Step-by-Step

It's a Post call analytics for your contact center with Amazon language AI services.  The link is here: https://aws.amazon.com/blogs/machine-learning/post-call-analytics-for-your-contact-center-with-amazon-language-ai-services/

## High-Level Architecture Diagram

```plaintext
[Call Recording Upload]  
       │  
       ▼  
[Amazon S3 (Input Bucket)]  
       │  
       ▼  
[AWS Lambda (Triggered by S3 Event)]  
       │  
       ▼  
[AWS Step Functions (Orchestrates Workflow)]  
       ├─▶ [Amazon Transcribe (Speech-to-Text)]  
       ├─▶ [Amazon Comprehend (Sentiment/Entity Detection)]  
       └─▶ [Optional: Amazon Bedrock (LLM Insights)]  
       │  
       ▼  
[Amazon S3 (Output Bucket - JSON Results)]  
       │  
       ▼  
[AWS Lambda (DynamoDB Metadata Sync)]  
       │  
       ▼  
[Amazon DynamoDB (Call Metadata)]  
       │  
       ▼  
[Web App (React/Angular/etc.)]  
       ├─▶ [Query DynamoDB for Call List]  
       └─▶ [Fetch Details from S3/JSON]
```

## Processing Flow Overview:

Call recording audio files are uploaded to the S3 bucket and folder, identified in the main stack outputs as InputBucket and InputBucketPrefix, respectively. The sample call recordings are automatically uploaded because you set the parameter loadSampleAudioFiles to true when you deployed PCA.

As each recording file is added to the input bucket, an S3 Event Notification triggers a Lambda function that initiates a workflow in Step Functions to process the file. The workflow orchestrates the steps to start an Amazon Transcribe batch job and process the results by doing entity detection and additional preparation of the call analytics results.  If enabled, the step functions will also generate insights using Amazon Bedrock or the LLM of your choice. Processed results are stored as JSON files in another S3 bucket and folder, identified in the main stack outputs as OutputBucket and OutputBucketPrefix.

As the Step Functions workflow creates each JSON results file in the output bucket, an S3 Event Notification triggers a Lambda function, which loads selected call metadata into a DynamoDB table.

The PCA UI web app queries the DynamoDB table to retrieve the list of processed calls to display on the home page. The call detail page reads additional detailed transcription and analytics from the JSON results file for the selected call.

Amazon S3 Lifecycle policies delete recordings and JSON files from both input and output buckets after a configurable retention period, defined by the deployment parameter RetentionDays. S3 Event Notifications and Lambda functions keep the DynamoDB table synchronized as files are both created and deleted.

When the EnableTranscriptKendraSearch parameter is true, the Step Functions workflow also adds time markers and metadata attributes to the transcription, which are loaded into an Amazon Kendra index. The transcription search web application is used to search call transcriptions.

## Detailed Component Breakdown

### 1. File Upload & Ingestion
User Uploads Audio:

- Web app uses S3 pre-signed URLs to securely upload call recordings to input-audio-bucket1379.

- Example file path: s3://input-audio-bucket1379/raw/call-1234.wav.

### 2. Event-Driven Processing
S3 Event Notification:

- Triggers Lambda when a new file is uploaded.

- Lambda validates the file (e.g., checks format/size) and starts the Step Functions workflow.

### 3. Step Functions Workflow
States:

1. Transcribe Audio:

    - Start an Amazon Transcribe batch job.

    - Output stored temporarily in S3 (transcript text).

2. Process Transcript:

    - Lambda function extracts speaker segments, timestamps, and normalizes text.

3. Analyze with Comprehend:

    - Detect sentiment (POSITIVE/NEGATIVE/NEUTRAL), entities (e.g., names, dates).

4. [Optional] Generate Insights with Bedrock:

    - Use an LLM (e.g., Claude) to summarize key issues or compliance risks.

5. Save Results:

    - Final JSON with all analytics saved to metadata-output-bucket1379.

    - Example path: s3://metadata-output-bucket1379/processed/call-1234.json.

### 4. Metadata Sync to DynamoDB
S3 Output Bucket Event:

- Triggers a Lambda function when a new JSON file is created.

- Lambda parses the JSON and writes critical metadata to DynamoDB

### 5. Web App Integration
Frontend:

- Queries DynamoDB via API Gateway/Lambda to display call lists.

- Example query: "Show all calls with negative sentiment from Agent-55 in May 2024."

- Detail View: Fetches the full JSON from S3 when a user selects a call.

### 6. Data Lifecycle & Security
- S3 Lifecycle Policies:

    - Automatically delete raw audio and JSON files after N days (e.g., 30 days).

- DynamoDB Cleanup:

    - S3 ObjectRemoved events trigger a Lambda to delete expired DynamoDB entries.

- Encryption:

    - S3 (AES-256), DynamoDB (AWS KMS), and TLS for data in transit.

### 7. Optional Components
- Amazon Kendra:

    - Indexes transcripts for natural language search (e.g., "Find calls mentioning 'refund policy'").

- QuickSight Dashboard:

    - Visualize trends (e.g., sentiment over time, common entities).

## Key AWS Services & Their Roles

| **Service**     | **Role**                                                                 |
|------------------|-------------------------------------------------------------------------|
| **S3**          | Stores raw audio, processed JSON results.                               |
| **Lambda**       | Serverless glue for triggers, data processing, and DynamoDB sync.      |
| **Step Functions** | Orchestrates Transcribe → Comprehend → Bedrock workflow.             |
| **Transcribe**   | Converts audio to text (supports speaker diarization).                 |
| **Comprehend**   | NLP for sentiment, entities, and PII detection.                        |
| **Bedrock**      | Generative AI for custom insights (e.g., compliance checks).           |
| **DynamoDB**     | Fast metadata store for call lists and filtering.                      |
| **IAM**          | Grants least-privilege access to resources.                            |
