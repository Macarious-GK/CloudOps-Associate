# Photo Upload & Presign Django App
## Overview
This Django app allows users to:
- Upload photos to an AWS S3 bucket.
- Generate presigned URLs for uploaded photos or existing S3 objects.

It also stores photo metadata (name, size, MIME type, S3 key) in a database table (Photo model).


## Environment Variables
Create a .env file in the project root:
```ini
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=

S3_BUCKET=
AWS_ROLE_ARN=
AWS_EXTERNAL_ID=
```

## APP Auth
- Create a User for the app with no permission but allow for sts-assume Role
- Create a Role with specific rules needed for the least privileged permission and with trust policy to the User used by the APP

## DB Creds
- Use Secret Manager to store RDS secrets 
- Retrieve secrets as Dict the use it.


## APIs
| Path           | View                | Description                    |
| -------------- | ------------------- | ------------------------------ |
| `/`            | `upload_page`       | Returns the upload page        |
| `/api/upload`  | `upload_photo_view` | Upload photo to S3             |
| `/api/presign` | `presign_key_view`  | Generate presigned URL for key |


## Upcoming
- Make Logs to CloudWatch