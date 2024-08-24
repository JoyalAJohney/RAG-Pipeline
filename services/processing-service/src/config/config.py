import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    PROCESSING_QUEUE_URL = os.getenv("PROCESSING_QUEUE_URL")
    EMBEDDING_QUEUE_URL = os.getenv("EMBEDDING_QUEUE_URL")

    S3_UPLOAD_BUCKET = os.getenv("S3_UPLOAD_BUCKET")
    S3_PROCESSED_BUCKET = os.getenv("S3_PROCESSED_BUCKET")
    
    DATABASE_URL = os.getenv("DATABASE_URL")