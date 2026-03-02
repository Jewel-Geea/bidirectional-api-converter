from fastapi import APIRouter, HTTPException
from src.models import GraphQLToRESTRequest, RESTToGraphQLRequest, ConversionResponse
from src.services.gql_to_rest_service import GraphQLToRESTService
from src.services.rest_to_gql_service import RESTToGraphQLService

router = APIRouter(prefix="/convert", tags=["conversion"])


@router.post("/gql-to-rest", response_model=ConversionResponse)
async def convert_graphql_to_rest(request: GraphQLToRESTRequest):
    try:
        service = GraphQLToRESTService()
        result = service.convert(request.schema_input)
        return ConversionResponse(spec=result["openapi"], code=result["fastapi_code"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rest-to-gql", response_model=ConversionResponse)
async def convert_rest_to_graphql(request: RESTToGraphQLRequest):
    try:
        service = RESTToGraphQLService()
        result = service.convert(request.openapi)
        return ConversionResponse(spec={"schema": result["schema"]}, code=result["resolver_code"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
