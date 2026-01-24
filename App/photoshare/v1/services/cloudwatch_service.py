import boto3

cloudwatch = boto3.client('cloudwatch')

def publish_upload_metric():
    cloudwatch.put_metric_data(
        Namespace='PhotoApp',
        MetricData=[
            {
                'MetricName': 'PhotoUploaded',
                'Value': 1,
                'Unit': 'Count'
            }
        ]
    )
