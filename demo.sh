#!/bin/bash

echo "🎬 API Converter Demo"
echo "===================="
echo ""

# Test 1: GraphQL to REST
echo "📝 Example 1: GraphQL → REST"
echo ""
echo "Input GraphQL Schema:"
echo "---------------------"
cat << 'EOF'
type Product {
  id: ID!
  name: String!
  price: Float!
  inStock: Boolean!
}

type Query {
  product(id: ID!): Product
  products: [Product!]!
}

type Mutation {
  createProduct(name: String!, price: Float!): Product!
  updateProduct(id: ID!, price: Float): Product!
  deleteProduct(id: ID!): Boolean!
}
EOF

echo ""
echo "Converting..."
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/convert/gql-to-rest \
  -H "Content-Type: application/json" \
  -d '{
    "schema": "type Product {\n  id: ID!\n  name: String!\n  price: Float!\n  inStock: Boolean!\n}\n\ntype Query {\n  product(id: ID!): Product\n  products: [Product!]!\n}\n\ntype Mutation {\n  createProduct(name: String!, price: Float!): Product!\n  updateProduct(id: ID!, price: Float): Product!\n  deleteProduct(id: ID!): Boolean!\n}"
  }')

echo "✅ Generated REST Endpoints:"
echo "$RESPONSE" | grep -o '"path":"[^"]*"' | sed 's/"path":"//g' | sed 's/"//g' | sort -u

echo ""
echo "✅ Generated FastAPI Code:"
echo "-------------------------"
echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['code'][:500])" 2>/dev/null || echo "See full output in UI"

echo ""
echo "================================"
echo ""

# Test 2: REST to GraphQL
echo "📝 Example 2: REST → GraphQL"
echo ""
echo "Input OpenAPI Spec:"
echo "-------------------"
cat << 'EOF'
{
  "openapi": "3.0.0",
  "paths": {
    "/products": {"get": {}, "post": {}},
    "/products/{id}": {"get": {}, "put": {}, "delete": {}}
  }
}
EOF

echo ""
echo "Converting..."
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/convert/rest-to-gql \
  -H "Content-Type: application/json" \
  -d '{
    "openapi": "{\"openapi\":\"3.0.0\",\"paths\":{\"/products\":{\"get\":{},\"post\":{}},\"/products/{id}\":{\"get\":{},\"put\":{},\"delete\":{}}}}"
  }')

echo "✅ Generated GraphQL Schema:"
echo "---------------------------"
echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['schema'])" 2>/dev/null || echo "See full output in UI"

echo ""
echo "================================"
echo ""
echo "🎉 Demo Complete!"
echo ""
echo "🌐 Try it yourself in the browser:"
echo "   http://localhost:5173"
echo ""
echo "📋 Copy/paste from examples/ folder:"
echo "   - examples/sample-schema.graphql"
echo "   - examples/sample-openapi.json"
