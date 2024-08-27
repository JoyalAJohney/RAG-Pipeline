

from pydantic import BaseModel
from typing import List, Optional



class RetrieveRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

    # Sample request body
    class Config:
        schema_extra = {
            "example": {
                "query": "What is the capital of France?",
                "top_k": 3
            }
        }



class RetrieveResponse(BaseModel):
    results: List[dict]
    combined_content: str

    # Sample response body
    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {
                        "content": "Paris is the capital of France.",
                        "source": "geography.pdf, Page 15",
                        "similarity": 0.95
                    }
                ],
                "combined_content": "Content: Paris is the capital of France.\nSource: geography.pdf, Page 15"
            }
        }


class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embedding: list[float]