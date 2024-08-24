import json
from ..logger import logger
from .chunk_handler import handle_chunks
from .file_processor import process_file
from ..aws.s3_handler import get_file_from_s3
from ..exceptions.exception import ProcessingError
from ..aws.sqs_handler import receive_message, delete_message


def process_jobs():
    logger.info("Starting to process jobs")
    while True:
        job = get_job()
        if job:
            process_job(job)


def get_job():
    logger.info("Polling Queue for messages...")
    message = receive_message()
    return message if message else None


def process_job(message):
    try:
        job_data = parse_job_data(message)
        
        logger.info(f"Processing file: {job_data['key']}")

        file_content = get_file_content(job_data)
        chunks = process_file(file_content, job_data['key'])
        
        handle_chunks(chunks, job_data)
        delete_message(message['ReceiptHandle'])

        logger.info(f"Processed file: {job_data['key']}")

    except ProcessingError as e:
        handle_error(e, message)
    except Exception as e:
        handle_error(e, message)


def parse_job_data(message):
    try:
        return json.loads(message['Body'])
    except json.JSONDecodeError as e:
        raise ProcessingError(f"Invalid job data: {str(e)}")


def get_file_content(job_data):
    file_content = get_file_from_s3(job_data['bucket'], job_data['key'])
    if not file_content:
        raise ProcessingError(f"Failed to retrieve file {job_data['key']} from S3")
    return file_content


def handle_error(error, message):
    logger.error(f"Error processing message: error - {str(error)}, message - {message}")
    # Implement dead-letter queue logic here