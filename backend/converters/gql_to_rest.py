from graphql import build_schema, GraphQLSchema
from typing import Dict, Any, List


def convert_graphql_to_rest(schema_sdl: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """Convert GraphQL schema to REST API specification and FastAPI code."""

    schema = build_schema(schema_sdl)

    endpoints = []
    routes_code = []

    # Process Query type
    query_type = schema.query_type
    if query_type:
        for field_name, field in query_type.fields.items():
            endpoint = process_query_field(field_name, field)
            endpoints.append(endpoint)
            routes_code.append(generate_route_code(endpoint))

    # Process Mutation type
    mutation_type = schema.mutation_type
    if mutation_type:
        for field_name, field in mutation_type.fields.items():
            endpoint = process_mutation_field(field_name, field)
            endpoints.append(endpoint)
            routes_code.append(generate_route_code(endpoint))

    # Generate OpenAPI spec
    openapi_spec = generate_openapi_spec(endpoints, schema)

    # Generate FastAPI code
    fastapi_code = generate_fastapi_code(routes_code, schema)

    return {"openapi": openapi_spec, "code": fastapi_code, "endpoints": endpoints}


def process_query_field(field_name: str, field) -> Dict[str, Any]:
    """Convert GraphQL query field to REST endpoint."""

    # Determine if it's a list or single item
    is_list = str(field.type).startswith("[")
    base_type = str(field.type).replace("[", "").replace("]", "").replace("!", "")

    # Build path
    if field.args:
        # Has arguments - likely a single item getter
        path = (
            f"/{base_type.lower()}s/{{id}}"
            if "id" in [arg for arg in field.args]
            else f"/{field_name}"
        )
    else:
        # No arguments - likely a list getter
        path = f"/{field_name}"

    return {
        "path": path,
        "method": "GET",
        "field_name": field_name,
        "return_type": base_type,
        "is_list": is_list,
        "args": {arg: str(field.args[arg].type) for arg in field.args},
    }


def process_mutation_field(field_name: str, field) -> Dict[str, Any]:
    """Convert GraphQL mutation field to REST endpoint."""

    base_type = str(field.type).replace("[", "").replace("]", "").replace("!", "")

    # Determine HTTP method based on naming convention
    if field_name.startswith("create"):
        method = "POST"
        path = f"/{base_type.lower()}s"
    elif field_name.startswith("update"):
        method = "PUT"
        path = f"/{base_type.lower()}s/{{id}}"
    elif field_name.startswith("delete"):
        method = "DELETE"
        path = f"/{base_type.lower()}s/{{id}}"
    else:
        method = "POST"
        path = f"/{field_name}"

    return {
        "path": path,
        "method": method,
        "field_name": field_name,
        "return_type": base_type,
        "is_list": False,
        "args": {arg: str(field.args[arg].type) for arg in field.args},
    }


def generate_route_code(endpoint: Dict[str, Any]) -> str:
    """Generate FastAPI route code for an endpoint."""

    method = endpoint["method"].lower()
    path = endpoint["path"]
    field_name = endpoint["field_name"]

    # Generate path parameters
    path_params = []
    if "{id}" in path:
        path_params.append("id: str")

    # Generate query/body parameters
    other_params = [
        f"{arg}: {map_graphql_type_to_python(type_)}"
        for arg, type_ in endpoint["args"].items()
        if arg != "id"
    ]

    all_params = ", ".join(path_params + other_params)

    code = f'''
@app.{method}("{path}")
def {field_name}({all_params}):
    """Auto-generated from GraphQL {field_name} field"""
    # TODO: Implement your business logic here
    return {{"message": "Not implemented"}}
'''
    return code


def map_graphql_type_to_python(graphql_type: str) -> str:
    """Map GraphQL types to Python types."""
    type_map = {"String": "str", "Int": "int", "Float": "float", "Boolean": "bool", "ID": "str"}

    clean_type = graphql_type.replace("!", "").replace("[", "").replace("]", "")
    return type_map.get(clean_type, "Any")


def generate_openapi_spec(endpoints: List[Dict], schema: GraphQLSchema) -> Dict[str, Any]:
    """Generate OpenAPI 3.0 specification."""

    paths = {}
    for endpoint in endpoints:
        path = endpoint["path"]
        method = endpoint["method"].lower()

        if path not in paths:
            paths[path] = {}

        paths[path][method] = {
            "summary": f"{endpoint['field_name']} endpoint",
            "responses": {
                "200": {
                    "description": "Successful response",
                    "content": {"application/json": {"schema": {"type": "object"}}},
                }
            },
        }

    return {
        "openapi": "3.0.0",
        "info": {"title": "Generated REST API", "version": "1.0.0"},
        "paths": paths,
    }


def generate_fastapi_code(routes: List[str], schema: GraphQLSchema) -> str:
    """Generate complete FastAPI application code."""

    code = """from fastapi import FastAPI
from typing import Any

app = FastAPI()

"""
    code += "\n".join(routes)

    return code
