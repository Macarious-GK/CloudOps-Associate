# myapp/aws_session.py
import boto3
import os
from dotenv import load_dotenv

load_dotenv() 

# Create a single session for the app
Iam_User = boto3.client("sts")

resp = Iam_User.assume_role(
    RoleArn=os.getenv("AWS_ROLE_ARN"),
    RoleSessionName="django-photoApp-session-identity",
    ExternalId= os.getenv("AWS_EXTERNAL_ID")
)
creds = resp['Credentials']
SESSION = boto3.Session(
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken'],
)

