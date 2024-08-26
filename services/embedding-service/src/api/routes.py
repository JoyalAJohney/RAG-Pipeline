
from ..utils.logger import logger
from fastapi import APIRouter, HTTPException
from .models import RetrieveRequest, RetrieveResponse
from ..services.retrieval_service import retrieve_documents
from ..utils.helper import format_results, combine_content

router = APIRouter()


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