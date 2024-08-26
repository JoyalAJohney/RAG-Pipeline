import chromadb
from ..config.config import Config
from ..utils.logger import logger


client = chromadb.HttpClient(
    host=Config.CHROMA_HOST,
    port=Config.CHROMA_PORT,
)

collection_name = "document_embedding"
collection = client.get_or_create_collection(collection_name)



def store_embedding(id, embedding, metadata, document):
    try:
        collection.add(
            embeddings=[embedding],
            documents=[document],
            metadatas=[metadata],
            ids=[id]
        )
        logger.info(f"Stored embedding for chunk: {id}")
        return True
    except Exception as e:
        logger.error(f"Error storing embedding: {str(e)}")
        return False



def query_embeddings(query_embedding, top_k=5):
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        return results
    except Exception as e:
        logger.error(f"Error querying embeddings: {str(e)}")
        return None