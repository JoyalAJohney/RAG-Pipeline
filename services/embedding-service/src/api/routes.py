
from ..utils.logger import logger
from fastapi import APIRouter, HTTPException, Response
from .models import RetrieveRequest, RetrieveResponse, EmbeddingResponse, EmbeddingRequest
from ..services.retrieval_service import retrieve_documents
from ..services.embedding_service import create_embedding
from ..utils.helper import format_results, combine_content

router = APIRouter()


@router.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return Response(content="OK", media_type="text/plain")


@router.post("/retrieve", response_model=RetrieveResponse)
def retrieve_endpoint(request: RetrieveRequest):
    try:
        results = retrieve_documents(request.query, request.top_k)
        if not results:
            raise HTTPException(status_code=500, detail="Failed to retrieve documents")
        
        formatted_results = format_results(results)
        combined = combine_content(formatted_results)
        
        return RetrieveResponse(results=formatted_results, combined_content=combined)
    except Exception as e:
        logger.error(f"Error in retrieve_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve documents")
    

@router.post("/embedding", response_model=EmbeddingResponse)
async def get_embedding(request: EmbeddingRequest):
    try:
        embedding = create_embedding(request.text)
        
        logger.info(f"Generated embedding for text: {request.text[:50]}... : {embedding[:5]}...")
        return EmbeddingResponse(embedding=embedding)
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate embedding")