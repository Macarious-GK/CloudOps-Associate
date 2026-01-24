import boto3
import json
import os

def get_rds_secret():
    secret_id = os.environ['RDS_SECRET_ID']
    client = boto3.client('secretsmanager')

    resp = client.get_secret_value(SecretId=secret_id)
    secret = json.loads(resp['SecretString'])

    return secret
