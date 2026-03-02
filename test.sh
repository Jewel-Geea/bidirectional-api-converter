#!/bin/bash

echo "🧪 Testing API Converter..."
echo ""

# Test 1: GraphQL to REST
echo "📝 Test 1: GraphQL → REST"
echo "Input: GraphQL schema with User type"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/convert/gql-to-rest \
  -H "Content-Type: application/json" \
  -d '{
    "schema": "type User {\n  id: ID!\n  name: String!\n}\n\ntype Query {\n  users: [User!]!\n}"
  }')

if echo "$RESPONSE" | grep -q "openapi"; then
  echo "✅ GraphQL → REST conversion: PASSED"
  echo "Generated endpoints:"
  echo "$RESPONSE" | grep -o '"path":"[^"]*"' | head -3
else
  echo "❌ GraphQL → REST conversion: FAILED"
  echo "$RESPONSE"
fi

echo ""
echo "---"
echo ""

# Test 2: REST to GraphQL
echo "📝 Test 2: REST → GraphQL"
echo "Input: OpenAPI spec with /users endpoint"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/convert/rest-to-gql \
  -H "Content-Type: application/json" \
  -d '{
    "openapi": "{\"openapi\":\"3.0.0\",\"paths\":{\"/users\":{\"get\":{}}}}"
  }')

if echo "$RESPONSE" | grep -q "schema"; then
  echo "✅ REST → GraphQL conversion: PASSED"
  echo "Generated schema includes:"
  echo "$RESPONSE" | grep -o 'type Query' | head -1
else
  echo "❌ REST → GraphQL conversion: FAILED"
  echo "$RESPONSE"
fi

echo ""
echo "---"
echo ""

# Test 3: Check frontend
echo "📝 Test 3: Frontend accessibility"
FRONTEND=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173)

if [ "$FRONTEND" = "200" ]; then
  echo "✅ Frontend: RUNNING (http://localhost:5173)"
else
  echo "❌ Frontend: NOT ACCESSIBLE"
fi

echo ""
echo "---"
echo ""

# Test 4: Check backend
echo "📝 Test 4: Backend health"
BACKEND=$(curl -s http://localhost:8000)

if echo "$BACKEND" | grep -q "API Converter"; then
  echo "✅ Backend: RUNNING (http://localhost:8000)"
else
  echo "❌ Backend: NOT ACCESSIBLE"
fi

echo ""
echo "🎉 All tests completed!"
echo ""
echo "🌐 Open http://localhost:5173 in your browser to use the app"
