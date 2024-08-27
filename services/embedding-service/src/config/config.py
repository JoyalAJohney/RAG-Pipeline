import os 
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Embedding service
    EMBEDDING_SERVICE_PORT = os.getenv("EMBEDDING_SERVICE_PORT")

    # AWS credentials
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    # AWS resources
    EMBEDDING_QUEUE_URL = os.getenv("EMBEDDING_QUEUE_URL")
    S3_PROCESSED_BUCKET = os.getenv("S3_PROCESSED_BUCKET")

    # Database
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    CHROMA_HOST = os.getenv("CHROMA_HOST")
    CHROMA_PORT = os.getenv("CHROMA_PORT")
    DATABASE_URL = os.getenv("DATABASE_URL")

    # AI models
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

    # API 
    API_PORT = os.getenv("API_PORT")