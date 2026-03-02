from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json

app = FastAPI(title="API Converter", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GraphQLToRESTRequest(BaseModel):
    schema: str
    options: Optional[Dict[str, Any]] = {}


class RESTToGraphQLRequest(BaseModel):
    openapi: str
    options: Optional[Dict[str, Any]] = {}


@app.get("/")
def root():
    return {"message": "API Converter - GraphQL ↔ REST"}


@app.post("/convert/gql-to-rest")
def graphql_to_rest(request: GraphQLToRESTRequest):
    try:
        from converters.gql_to_rest import convert_graphql_to_rest

        result = convert_graphql_to_rest(request.schema, request.options)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/convert/rest-to-gql")
def rest_to_graphql(request: RESTToGraphQLRequest):
    try:
        from converters.rest_to_gql import convert_rest_to_graphql

        result = convert_rest_to_graphql(request.openapi, request.options)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
