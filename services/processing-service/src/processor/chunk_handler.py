import uuid
import json
from ..logger import logger
from ..config.config import Config
from ..aws.s3_handler import upload_to_s3
from ..exceptions.exception import ProcessingError
from ..aws.sqs_handler import send_message_to_queue


def handle_chunks(chunks, job_data):
    chunk_refs = upload_chunks_to_s3(chunks, job_data)
    if chunk_refs:
        send_chunk_refs_to_queue(chunk_refs, job_data)
    else:
        raise ProcessingError(f"Failed to upload chunks for file {job_data['key']}")


def upload_chunks_to_s3(chunks, job_data):
    chunk_refs = []
    job_id = job_data.get('job_id', str(uuid.uuid4()))

    for i, chunk in enumerate(chunks):
        chunk_id = f"{job_id}_{i}"
        s3_key = f"chunks/{job_id}/{chunk_id}.json"
        
        if upload_to_s3(json.dumps(chunk), Config.S3_PROCESSED_BUCKET, s3_key):
            chunk_refs.append({
                'chunk_id': chunk_id,
                's3_key': s3_key,
                'page_num': chunk['page_num'],
                'chunk_num': chunk['chunk_num']
            })
        else:
            logger.error(f"Failed to upload chunk {i} to S3. Skipping this chunk.")
    
    return chunk_refs



def send_chunk_refs_to_queue(chunk_refs, job_data):
    message = {
        'job_id': job_data.get('job_id', str(uuid.uuid4())),
        'file_name': job_data['key'],
        'total_chunks': len(chunk_refs),
        'chunk_refs': chunk_refs
    }
    return send_message_to_queue(message, Config.EMBEDDING_QUEUE_URL)