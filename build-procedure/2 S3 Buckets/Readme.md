## Summary of Bucket Configurations

| **Bucket Name**             | **Purpose**              | **Key Policies**                                                                                   |
|------------------------------|--------------------------|----------------------------------------------------------------------------------------------------|
| **input-audio-bucket1379**   | Raw audio uploads        | Block public access; allow Lambda/Step Functions read; enforce encryption.                        |
| **metadata-output-bucket1379** | Processed JSON results | Block public access; allow Step Functions write, Lambda read; optional CORS.                      |
| **web-app-bucket1379**       | Host web app             | Public read for static assets; static website hosting enabled.                                    |

# 1. Input Audio Bucket
Name: input-audio-bucket1379
Purpose: Stores raw audio files (call recordings) uploaded by users or systems.

### Permissions
- Write: Web app users (via pre-signed URLs or IAM roles).

- Read: Lambda (ProcessUploadAudio) and Step Functions.

- Triggers: Lambda (ProcessUploadAudio) on s3:ObjectCreated:*.

### Additional Settings
- CORS: Not needed (uploads via pre-signed URLs don’t require CORS).

- Lifecycle Policy: Delete files after X days (e.g., 7 days).

- Versioning: Enabled (optional for recovery).

- Server Access Logging: Log to metadata-output-bucket1379/logs/input-bucket/.

# 2. Metadata Output Bucket
Name: metadata-output-bucket1379
Purpose: Stores processed JSON results (transcriptions, sentiment analysis, etc.).

### Permissions
- Write: Step Functions workflow.

- Read: Lambda (SyncToDynamoDB).

- Triggers: Lambda (SyncToDynamoDB) on s3:ObjectCreated:*.

### Additional Settings
- CORS: Only if your web app directly fetches JSON files (example below).

- Lifecycle Policy: Delete files after X days (matches input bucket).

- Versioning: Optional.

# 3. Web App Bucket
Name: web-app-bucket1379
Purpose: Hosts static files for the web interface (HTML/CSS/JS).

### Permissions
- Write: CI/CD pipeline or developers (via IAM roles).

- Read: Public (for static web content).

### Additional Settings
- Static Website Hosting: Enabled (index: index.html, error: error.html).

- CORS: Configure if your web app interacts with S3 or APIs directly.