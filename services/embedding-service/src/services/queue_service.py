import json
import asyncio
from ..utils.logger import logger
from ..config.config import Config
from .embedding_service import create_embedding
from ..aws.s3_handler import get_s3_object
from ..aws.sqs_handler import receive_message, delete_message
from ..database.vector_db import store_embedding




def process_queue():
    while True:
        logger.info("Checking for messages...")
        try:
            message = receive_message()
            if message:
                logger.info(f"Processing message: {message['MessageId']}")
                process_message(message)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")


def process_message(message):
    try:
        body = json.loads(message['Body'])
        job_id, file_name, original_file_name, chunk_refs = parse_message_body(body)

        all_chunks_processed = True
        for chunk_ref in chunk_refs:
            try:
                success = process_chunk(job_id, file_name, original_file_name, chunk_ref)
                if not success:
                    logger.error(f"Failed to process chunk {chunk_ref['chunk_id']}")
                    all_chunks_processed = False
            except Exception as e:
                logger.error(f"Error processing chunk {chunk_ref['chunk_id']}: {str(e)}")
                all_chunks_processed = False
        
        if all_chunks_processed:
            logger.info(f"Processed all chunks for job: {job_id}")
            delete_message(message['ReceiptHandle'])
        else:
            logger.warning(f"Failed to process all chunks for job: {job_id}")
        
    except Exception as e:
        logger.error(f"Error processing message {message['MessageId']}: {str(e)}")
        return False



def parse_message_body(body):
    job_id = body['job_id']
    file_name = body['file_name']
    original_file_name = file_name.split('_', 1)[1]  # remove job Id prefix
    chunk_refs = body['chunk_refs']
    return job_id, file_name, original_file_name, chunk_refs




def process_chunk(job_id, file_name, original_file_name, chunk_ref):
    chunk = get_chunk_content_from_s3(chunk_ref)
    if not chunk:
        return False
    
    chunk_text = chunk['content'].replace('\n', ' ') # remove newlines, reduce context window

    embedding = create_embedding(chunk_text)
    if not embedding:
        logger.error(f"Failed to create embedding for chunk: {chunk_ref['chunk_id']}")
        return False
    
    metadata = prepare_metadata(job_id, file_name, original_file_name, chunk_ref, chunk)

    success = store_embedding(chunk_ref['chunk_id'], embedding, metadata, chunk_text)
    if not success:
        logger.error(f"Failed to add embedding to collection for chunk: {chunk_ref['chunk_id']}")
        return False

    return True  




def get_chunk_content_from_s3(chunk_ref):
    logger.info(f"Getting chunk from S3: {chunk_ref['s3_key']}")
    chunk_content = get_s3_object(Config.S3_PROCESSED_BUCKET, chunk_ref['s3_key'])
    if not chunk_content:
        logger.error(f"Failed to get chunk from S3: {chunk_ref['s3_key']}")
        return None

    return json.loads(chunk_content)




def prepare_metadata(job_id, file_name, original_file_name, chunk_ref, chunk):
    logger.info(f"Preparing metadata for chunk: {chunk_ref['chunk_id']}")
    metadata = {
        "job_id": job_id,
        "chunk_id": chunk_ref['chunk_id'],
        "system_file_name": file_name,
        "original_file_name": original_file_name,
        "page_number": chunk['page_num'],
        "chunk_number": chunk['chunk_num'],
    }
    return metadata  