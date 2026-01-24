# myapp/aws_clients.py
from .aws_session import SESSION

S3_CLIENT = SESSION.client('s3')

