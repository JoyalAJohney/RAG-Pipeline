
from ..utils.logger import logger
from ..database.vector_db import query_embeddings
from .embedding_service import create_embedding


def retrieve_documents(query, top_k=5):
    query_embedding = create_embedding(query)
    if query_embedding is None:
        logger.error("Error creating query embedding")
        return None
    
    results = query_embeddings(query_embedding, top_k)
    if results is None:
        logger.error("Error querying embeddings")
        return None
    
    # reranked_results = rerank(query, results)
    return results



def rerank(query, results):
    # Implement re-ranking logic here
    return sorted(results, key=lambda x: x['distance'])