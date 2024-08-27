from fastapi import FastAPI
from src.schema.pydantic_schema import QueryInput, QueryResponse, UpsertVectorRequest
from src.api.api_services import Services
from src.utils.qdrant_utils import QdrantUtils

service = Services(qdrant_client=QdrantUtils())
app = FastAPI()

@app.post("/query",response_model=QueryResponse)
async def query(input: QueryInput):
    response = await service.route_user_query(query=input.query)
    return QueryResponse(status="200",response=response)

@app.post("/upsert_qdrant")
async def upsert_pinecone(input: UpsertVectorRequest):
    return await service.upsert_vectors(file_path=input.file_path,collection_name=input.collection_name)
    
    
