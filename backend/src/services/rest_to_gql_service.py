import json
from typing import Any, Dict, List


class RESTToGraphQLService:
    """Service for converting REST APIs to GraphQL schemas."""

    def convert(self, openapi_json: str) -> Dict[str, Any]:
        spec = json.loads(openapi_json)
        queries, mutations, types = self._extract_operations(spec)
        schema = self._generate_schema(types, queries, mutations)
        resolver_code = self._generate_resolvers(queries, mutations)
        return {"schema": schema, "resolver_code": resolver_code}

    def _extract_operations(self, spec: Dict) -> tuple:
        queries = []
        mutations = []
        types: Dict[str, Any] = {}

        for path, methods in spec.get("paths", {}).items():
            for method, details in methods.items():
                if method.upper() == "GET":
                    queries.append(self._process_get(path, details))
                else:
                    mutations.append(self._process_mutation(path, method, details))

        return queries, mutations, types

    def _process_get(self, path: str, details: Dict) -> Dict[str, Any]:
        name = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
        has_id = "{" in path
        return {
            "name": name,
            "args": "id: ID!" if has_id else "",
            "return_type": "JSON",
            "path": path,
            "method": "GET",
        }

    def _process_mutation(self, path: str, method: str, details: Dict) -> Dict[str, Any]:
        name = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
        return {
            "name": f"{method.lower()}_{name}",
            "args": "input: JSON!",
            "return_type": "JSON",
            "path": path,
            "method": method.upper(),
        }

    def _generate_schema(self, types: Dict, queries: List[Dict], mutations: List[Dict]) -> str:
        schema = "scalar JSON\n\n"

        if queries:
            schema += "type Query {\n"
            for q in queries:
                args = f"({q['args']})" if q["args"] else ""
                schema += f"  {q['name']}{args}: {q['return_type']}\n"
            schema += "}\n\n"

        if mutations:
            schema += "type Mutation {\n"
            for m in mutations:
                args = f"({m['args']})" if m["args"] else ""
                schema += f"  {m['name']}{args}: {m['return_type']}\n"
            schema += "}\n"

        return schema

    def _generate_resolvers(self, queries: List[Dict], mutations: List[Dict]) -> str:
        code = """import strawberry
from typing import Optional
import httpx

BASE_URL = "http://localhost:8000"

@strawberry.type
class Query:
"""
        for q in queries:
            args = "id: str" if q["args"] else ""
            code += f"""
    @strawberry.field
    async def {q['name']}(self{', ' + args if args else ''}) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{{BASE_URL}}{q['path']}")
            return response.json()
"""

        if mutations:
            code += """
@strawberry.type
class Mutation:
"""
            for m in mutations:
                code += f"""
    @strawberry.mutation
    async def {m['name']}(self, input: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.{m['method'].lower()}(f"{{BASE_URL}}{m['path']}", json=input)
            return response.json()
"""

        code += "\nschema = strawberry.Schema(query=Query"
        if mutations:
            code += ", mutation=Mutation"
        code += ")\n"

        return code
