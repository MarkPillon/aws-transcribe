aws s3api put-bucket-cors \
  --bucket metadata-output-bucket1379 \
  --cors-configuration '{
    "CORSRules": [{
      "AllowedOrigins": ["https://your-web-app-domain.com"],
      "AllowedMethods": ["GET"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }]
  }'