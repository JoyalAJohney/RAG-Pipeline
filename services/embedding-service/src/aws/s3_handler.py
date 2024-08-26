import boto3
from ..utils.logger import logger
from ..config.config import Config

s3 = boto3.client('s3', 
    region_name=Config.AWS_REGION,
    endpoint_url=Config.AWS_ENDPOINT_URL,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
)


def get_s3_object(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        logger.error(f"Error reading from S3: {e}")
        return None
