import openai
from ..config.config import Config
from ..utils.logger import logger



def create_embedding(text):
    openai.api_key = Config.OPENAI_API_KEY
    
    try:
        logger.info(f"Creating embedding for: {text}")
        response = openai.Embedding.create(input=text, model=Config.EMBEDDING_MODEL)
        return response['data'][0]['embedding']
    except Exception as e:
        logger.error(f"Error creating embedding: {str(e)}")
        return None