import json
from typing import Dict, Any


def convert_rest_to_graphql(openapi_json: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """Convert OpenAPI/REST spec to GraphQL schema and resolver code."""

    spec = json.loads(openapi_json)

    types = {}
    queries = []
    mutations = []

    # Process paths
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if method.upper() == "GET":
                query = process_get_endpoint(path, details)
                queries.append(query)
            elif method.upper() in ["POST", "PUT", "DELETE"]:
                mutation = process_mutation_endpoint(path, method, details)
                mutations.append(mutation)

    # Generate GraphQL schema
    schema_sdl = generate_graphql_schema(types, queries, mutations)

    # Generate resolver code
    resolver_code = generate_resolver_code(queries, mutations)

    return {"schema": schema_sdl, "code": resolver_code, "queries": queries, "mutations": mutations}


def process_get_endpoint(path: str, details: Dict) -> Dict[str, Any]:
    """Convert GET endpoint to GraphQL query."""

    # Extract resource name from path
    parts = [p for p in path.split("/") if p and not p.startswith("{")]
    resource_name = parts[-1] if parts else "data"

    # Check if it's a single item or list
    has_id = "{id}" in path

    return {
        "name": resource_name.rstrip("s") if has_id else resource_name,
        "type": resource_name.rstrip("s").capitalize(),
        "is_list": not has_id,
        "path": path,
        "method": "GET",
    }


def process_mutation_endpoint(path: str, method: str, details: Dict) -> Dict[str, Any]:
    """Convert POST/PUT/DELETE endpoint to GraphQL mutation."""

    parts = [p for p in path.split("/") if p and not p.startswith("{")]
    resource_name = parts[-1] if parts else "data"
    type_name = resource_name.rstrip("s").capitalize()

    # Determine mutation name
    if method.upper() == "POST":
        mutation_name = f"create{type_name}"
    elif method.upper() == "PUT":
        mutation_name = f"update{type_name}"
    else:  # DELETE
        mutation_name = f"delete{type_name}"

    return {"name": mutation_name, "type": type_name, "path": path, "method": method.upper()}


def generate_graphql_schema(types: Dict, queries: List[Dict], mutations: List[Dict]) -> str:
    """Generate GraphQL SDL schema."""

    schema = ""

    # Generate Query type
    if queries:
        schema += "type Query {\n"
        for query in queries:
            return_type = f"[{query['type']}!]!" if query["is_list"] else query["type"]
            args = "(id: ID!)" if not query["is_list"] else ""
            schema += f"  {query['name']}{args}: {return_type}\n"
        schema += "}\n\n"

    # Generate Mutation type
    if mutations:
        schema += "type Mutation {\n"
        for mutation in mutations:
            if "delete" in mutation["name"].lower():
                schema += f"  {mutation['name']}(id: ID!): Boolean!\n"
            else:
                schema += (
                    f"  {mutation['name']}(input: {mutation['type']}Input!): {mutation['type']}!\n"
                )
        schema += "}\n\n"

    # Generate placeholder types
    type_names = set([q["type"] for q in queries] + [m["type"] for m in mutations])
    for type_name in type_names:
        schema += f"type {type_name} {{\n"
        schema += f"  id: ID!\n"
        schema += f"  # Add your fields here\n"
        schema += f"}}\n\n"

        schema += f"input {type_name}Input {{\n"
        schema += f"  # Add your input fields here\n"
        schema += f"}}\n\n"

    return schema


def generate_resolver_code(queries: List[Dict], mutations: List[Dict]) -> str:
    """Generate Python resolver code using Strawberry."""

    code = """import strawberry
import httpx
from typing import List, Optional

BASE_URL = "http://localhost:8000"  # Change to your REST API URL

"""

    # Generate type definitions
    code += """@strawberry.type
class PlaceholderType:
    id: str
    # Add your fields here

"""

    # Generate Query resolvers
    if queries:
        code += "@strawberry.type\nclass Query:\n"
        for query in queries:
            if query["is_list"]:
                code += f"""    @strawberry.field
    async def {query['name']}(self) -> List[PlaceholderType]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{{BASE_URL}}{query['path']}")
            return response.json()
    
"""
            else:
                path_template = query["path"].replace("{id}", "{id_value}")
                code += f"""    @strawberry.field
    async def {query['name']}(self, id: str) -> PlaceholderType:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{{{{BASE_URL}}}}{path_template}".replace('{{{{id_value}}}}', id))
            return response.json()
    
"""

    # Generate Mutation resolvers
    if mutations:
        code += "@strawberry.type\nclass Mutation:\n"
        for mutation in mutations:
            code += f"""    @strawberry.mutation
    async def {mutation['name']}(self, id: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.{mutation['method'].lower()}(f"{{BASE_URL}}{mutation['path']}")
            return response.status_code == 200
    
"""

    code += """
schema = strawberry.Schema(query=Query, mutation=Mutation)
"""

    return code
