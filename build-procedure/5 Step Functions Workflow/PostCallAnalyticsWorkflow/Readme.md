# Step Functions Workflow Overview
Name: PostCallAnalyticsWorkflow
Purpose: Orchestrates audio processing, transcription, NLP analysis, and result storage.
Services Used:

- Amazon Transcribe (speech-to-text)

- Amazon Comprehend (sentiment/entity detection)

- Amazon S3 (input/output buckets)

- (Optional) Amazon Bedrock (LLM insights)

# Key Workflow States Explained
### 1. StartTranscriptionJob:

- Starts a Transcribe job for the audio file in input-audio-bucket1379.

- Includes retries for job conflicts (e.g., duplicate job names).

### 2. CheckTranscriptionStatus:

- Polls Transcribe until the job completes (retries 10x with 30-second intervals).

### 3. ProcessTranscript:

- (Optional) Invokes a Lambda to format the raw transcript (e.g., split speaker turns).

### 4. DetectSentiment:

- Uses Amazon Comprehend to analyze sentiment (POSITIVE/NEGATIVE/NEUTRAL).

### 5. GenerateInsights:

- (Optional) Invokes a Lambda to generate insights via Amazon Bedrock (e.g., "What was the customer's main complaint?").

### 6. SaveResults:

- Stores the final JSON (transcript, sentiment, insights) in metadata-output-bucket1379.

# Step Functions Execution Role
Role Name: PCA-StepFunctions-Role
Permissions:

- transcribe:StartTranscriptionJob

- transcribe:GetTranscriptionJob

- comprehend:DetectSentiment

- s3:PutObject (for metadata-output-bucket1379)

- lambda:InvokeFunction (if using Bedrock/Lambda)

## Error Handling
Retries:

- Transcribe job status checks retry 10 times with 30-second intervals.

- Lambda invocations retry 3 times for service exceptions.

Fallbacks:

- Bedrock insights are optional; failures don’t block the workflow.