from typing import Dict, Any
from pydantic import BaseModel, Field


class GraphQLToRESTRequest(BaseModel):
    schema_input: str = Field(..., min_length=1, alias="schema")


class RESTToGraphQLRequest(BaseModel):
    openapi: str = Field(..., min_length=1)


class ConversionResponse(BaseModel):
    spec: Dict[str, Any]
    code: str
