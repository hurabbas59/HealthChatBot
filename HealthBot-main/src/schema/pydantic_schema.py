from pydantic import BaseModel

class QueryInput(BaseModel):
    query: str


class QueryResponse(BaseModel):
    status: str
    response: str


class UpsertVectorRequest(BaseModel):
    collection_name: str
    file_path : str