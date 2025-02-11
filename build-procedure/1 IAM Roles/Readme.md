# Summary Table

| **Role Name**           | **Service**             | **Key Permissions**                          | **Trusted Entity**            |
|--------------------------|-------------------------|----------------------------------------------|--------------------------------|
| **PCA-Lambda-Role**      | Lambda Functions       | S3, Step Functions, DynamoDB, CloudWatch    | `lambda.amazonaws.com`        |
| **PCA-StepFunctions-Role** | Step Functions       | Transcribe, Comprehend, S3, Lambda Invoke   | `states.amazonaws.com`        |


## Key Security Best Practices
Least Privilege: Roles only have permissions needed for their specific tasks.

Encryption Enforcement:

S3 uploads require AES256 encryption.

Use KMS keys (aws:kms) for stricter control.

Secure Transport: Block HTTP traffic via bucket policies.

Resource-Level Restrictions: Limit access to specific buckets/tables.