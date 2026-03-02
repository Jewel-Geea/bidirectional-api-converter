from typing import Any, Dict, List
from graphql import build_schema, GraphQLSchema


class GraphQLToRESTService:
    """Service for converting GraphQL schemas to REST APIs."""

    def convert(self, schema_sdl: str) -> Dict[str, Any]:
        schema = build_schema(schema_sdl)
        endpoints = self._extract_endpoints(schema)
        openapi_spec = self._generate_openapi(endpoints, schema)
        fastapi_code = self._generate_code(endpoints, schema)
        return {"openapi": openapi_spec, "fastapi_code": fastapi_code}

    def _extract_endpoints(self, schema: GraphQLSchema) -> List[Dict[str, Any]]:
        endpoints = []
        if schema.query_type:
            for field_name, field in schema.query_type.fields.items():
                endpoints.append(self._process_query(field_name, field))
        if schema.mutation_type:
            for field_name, field in schema.mutation_type.fields.items():
                endpoints.append(self._process_mutation(field_name, field))
        return endpoints

    def _process_query(self, field_name: str, field) -> Dict[str, Any]:
        params = {arg: str(field.args[arg].type) for arg in field.args}
        return {
            "path": f"/{field_name.lower()}s" if not params else f"/{field_name.lower()}s/{{id}}",
            "method": "GET",
            "operation": field_name,
            "params": params,
            "return_type": str(field.type),
        }

    def _process_mutation(self, field_name: str, field) -> Dict[str, Any]:
        params = {arg: str(field.args[arg].type) for arg in field.args}
        method = "POST"
        path = f"/{field_name.replace('create', '').replace('Create', '').lower()}s"

        if "update" in field_name.lower():
            method = "PUT"
            path = f"{path}/{{id}}"
        elif "delete" in field_name.lower():
            method = "DELETE"
            path = f"{path}/{{id}}"

        return {
            "path": path,
            "method": method,
            "operation": field_name,
            "params": params,
            "return_type": str(field.type),
        }

    def _generate_openapi(self, endpoints: List[Dict], schema: GraphQLSchema) -> Dict[str, Any]:
        paths: Dict[str, Any] = {}
        for endpoint in endpoints:
            path = endpoint["path"]
            if path not in paths:
                paths[path] = {}
            paths[path][endpoint["method"].lower()] = {
                "summary": endpoint["operation"],
                "responses": {"200": {"description": "Success"}},
            }
        return {"openapi": "3.0.0", "info": {"title": "API", "version": "1.0.0"}, "paths": paths}

    def _generate_code(self, endpoints: List[Dict[str, Any]], schema: GraphQLSchema) -> str:
        routes = [self._generate_route(e) for e in endpoints]
        return f"""from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

{chr(10).join(routes)}
"""

    def _generate_route(self, endpoint: Dict[str, Any]) -> str:
        method = endpoint["method"].lower()
        path = endpoint["path"]
        operation = endpoint["operation"]
        params = endpoint["params"]

        path_params = [p.strip("{}") for p in path.split("/") if "{" in p]
        body_params = [p for p in params if p not in path_params]

        func_params = ", ".join([f"{p}: str" for p in path_params])
        if body_params:
            func_params += ", data: dict" if func_params else "data: dict"

        return f"""
@app.{method}("{path}")
async def {operation}({func_params}):
    return {{"message": "Not implemented"}}
"""
