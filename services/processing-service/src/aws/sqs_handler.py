import boto3
import json
from ..logger import logger
from botocore.exceptions import ClientError
from ..config.config import Config

sqs = boto3.client('sqs', 
    region_name=Config.AWS_REGION,
    endpoint_url=Config.AWS_ENDPOINT_URL,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY                   
)


def receive_message():
    try:
        response = sqs.receive_message(
            QueueUrl=Config.PROCESSING_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        messages = response.get('Messages', [])
        logger.info(f"Received messages from SQS: {messages}")
        return messages[0] if messages else None
    except ClientError as e:
        logger.error(f"Error receiving message from SQS: {str(e)}")
        return None


def delete_message(receipt_handle):
    try:
        sqs.delete_message(
            QueueUrl=Config.PROCESSING_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
        return True 
    except ClientError as e:
        logger.error(f"Error deleting message from SQS: {str(e)}")
        return False


def send_message_to_queue(message, queue_url):
    try:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        return True
    except ClientError as e:
        logger.error(f"Error sending message to SQS: {str(e)}")
        return False