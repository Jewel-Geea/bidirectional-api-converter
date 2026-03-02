# 🎬 Quick Demo Guide

## Step 1: Start the App

```bash
npm run dev
```

This starts both backend (port 8000) and frontend (port 5173)

## Step 2: Open Browser

Go to: **http://localhost:5173**

## Step 3: Try GraphQL → REST

### Copy this GraphQL schema:

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
}

type Post {
  id: ID!
  title: String!
  content: String!
  authorId: ID!
}

type Query {
  user(id: ID!): User
  users: [User!]!
  post(id: ID!): Post
  posts: [Post!]!
}

type Mutation {
  createUser(name: String!, email: String!, age: Int): User!
  updateUser(id: ID!, name: String, email: String): User!
  deleteUser(id: ID!): Boolean!
  
  createPost(title: String!, content: String!, authorId: ID!): Post!
  deletePost(id: ID!): Boolean!
}
```

### What you'll get:

**REST Endpoints:**
- `GET /users` - Get all users
- `GET /users/{id}` - Get user by ID
- `POST /users` - Create user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user
- `GET /posts` - Get all posts
- `GET /posts/{id}` - Get post by ID
- `POST /posts` - Create post
- `DELETE /posts/{id}` - Delete post

**Plus complete FastAPI code!**

## Step 4: Try REST → GraphQL

### Click "REST → GraphQL" button

### Copy this OpenAPI spec:

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Blog API",
    "version": "1.0.0"
  },
  "paths": {
    "/users": {
      "get": {
        "summary": "Get all users"
      },
      "post": {
        "summary": "Create user"
      }
    },
    "/users/{id}": {
      "get": {
        "summary": "Get user by ID"
      }
    },
    "/posts": {
      "get": {
        "summary": "Get all posts"
      }
    }
  }
}
```

### What you'll get:

**GraphQL Schema:**
```graphql
type Query {
  users: [User!]!
  user(id: ID!): User
  posts: [Post!]!
}

type Mutation {
  createUser(input: UserInput!): User!
}
```

**Plus Strawberry resolver code!**

## 🎯 What to Notice

1. **Smart Mapping:**
   - `createX` → POST
   - `updateX` → PUT
   - `deleteX` → DELETE
   - Queries → GET

2. **Type Preservation:**
   - GraphQL `String!` → Python `str`
   - GraphQL `Int` → Python `int`
   - GraphQL `ID!` → Python `str`

3. **Complete Code:**
   - Not just specs, but working implementations
   - FastAPI routes with decorators
   - Strawberry resolvers with async/await

## 📸 Screenshot This!

Perfect for LinkedIn:
- The UI showing input/output
- Generated FastAPI code
- Generated GraphQL schema
- Terminal showing both servers running

---

**That's it!** You now have a working bi-directional API converter. 🚀
