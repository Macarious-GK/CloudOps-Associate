import boto3
from botocore.exceptions import ClientError
import os
import uuid
from dotenv import load_dotenv
import json
# Load .env variables
load_dotenv() 

####################### AWS Configuration ###########################
Iam_User = boto3.client("sts")
print(Iam_User.get_caller_identity().get('Arn'))

####################### STS IAM Role #############################
resp = Iam_User.assume_role(
    RoleArn=os.getenv("AWS_ROLE_ARN"),
    RoleSessionName="django-photoApp-session-identity",
    ExternalId= os.getenv("AWS_EXTERNAL_ID")
)
creds = resp['Credentials']
session = boto3.Session(
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken'],
)
print(session.client('sts').get_caller_identity().get('Arn'))
####################### s3 Client ###################################
# List S3 Buckets
# Upload a file
# Create presigned URL

def List_S3_Buckets(s3_client):
    buckets = s3_client.list_buckets()
    return buckets['Buckets']

def upload_photo(s3_client, bucket, file_obj, content_type):
    key = f"photos/{file_obj.name}"

    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=file_obj,
        ContentType=content_type
    )
    return key

def generate_presigned_url(s3_client, bucket, key, expiration=3600):
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )
    return url


s3_client = session.client('s3')
buckets = generate_presigned_url(s3_client, os.getenv('S3_BUCKET'), 'photos/bc3595d9-a1da-46f0-aaff-2f016ade33dc')

####################### Secrets Manager Client ######################

def get_secret(secret_name):

    secret_name = secret_name

    # Create a Secrets Manager client
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

get_secret("mac/heart/inner")
secret_out = get_secret("mac/heart/inner/db")
secret_out_dict = json.loads(secret_out)
print(secret_out_dict['username'])
# ####################### Parameter Store Client ######################
# ssm_client = session.client('ssm')
# param = ssm_client.get_parameter(
#     Name=os.getenv('RDS_PARAM_STORE_NAME'),
#     WithDecryption=True
# )
####################### CloudWatch Client ###########################
# retrive secrets from secret manager
# retrive config from parameter store
# put cloudwatch metric
