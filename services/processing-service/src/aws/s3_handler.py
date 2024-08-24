import boto3
from ..logger import logger
from botocore.exceptions import ClientError
from ..config.config import Config

s3 = boto3.client('s3', 
    region_name=Config.AWS_REGION,
    endpoint_url=Config.AWS_ENDPOINT_URL,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
)

def get_file_from_s3(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    except ClientError as e:
        logger.error(f"Error getting file from S3: {str(e)}")
        return None


def upload_to_s3(content, bucket, key):
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=content)
        logger.info(f"Uploaded file to s3://{bucket}/{key}")
        return True
    except ClientError as e:
        logger.error(f"Error uploading file to S3: {str(e)}")
        return False