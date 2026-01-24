from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Photo
from .aws_clients import S3_CLIENT

import json
import os
import uuid
from dotenv import load_dotenv

load_dotenv() 

def upload_page(request):
    return render(request, 'photos/upload.html')

@csrf_exempt
def upload_photo_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    file = request.FILES.get('photo')
    if not file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    try:
        key = f"photos/{file.name}"  # S3 key
        S3_CLIENT.put_object(
            Bucket=os.environ.get('S3_BUCKET'),
            Key=key,
            Body=file.file,
            ContentType=file.content_type
        )

        filename = os.path.basename(file.name)
        presigned_url = S3_CLIENT.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': os.environ.get('S3_BUCKET'),
                'Key': key,
            },
            ExpiresIn=3600
        )

        # Save to RDS
        photo = Photo.objects.create(
            s3_key=key,
            file_name=file.name,
            file_size=file.size,
            mime_type=file.content_type,
        )

        return JsonResponse({
            'id': photo.id,
            'presigned_url': presigned_url
        })

    except Exception as e:
        return JsonResponse({'error': 'Failed to upload to S3', 'details': str(e)}, status=500)


@csrf_exempt
def presign_key_view(request):
    """Generate presigned URL for an existing key"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    bucket_name = os.environ.get('S3_BUCKET')

    try:
        data = json.loads(request.body.decode('utf-8'))
        key = data.get('key')
        if not key:
            return JsonResponse({'error': 'No key provided'}, status=400)
        key = f"photos/{key}"
        try:
            S3_CLIENT.head_object(Bucket=bucket_name, Key=key)
        except S3_CLIENT.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ['404', 'NoSuchKey']:
                return JsonResponse({'error': 'S3 key does not exist, Check your key'}, status=404)
            else:
                return JsonResponse({'error': 'S3 error', 'details': str(e)}, status=500)

        filename = os.path.basename(key)
        presigned_url = S3_CLIENT.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': key,
               
            },
            ExpiresIn=3600
        )
        print("Presigned URL2:", presigned_url)

        return JsonResponse({'presigned_url': presigned_url})

    except Exception as e:
        return JsonResponse({
            'error': 'Failed to generate presigned URL',
            'details': str(e)
        }, status=500)
