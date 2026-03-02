# API Converter - GraphQL ↔ REST

Bi-directional API converter that transforms GraphQL schemas to REST APIs and vice versa, with auto-generated production-ready code.

## ✨ Features

- 🔄 **GraphQL → REST**: Convert GraphQL schemas to REST endpoints + FastAPI code
- 🔄 **REST → GraphQL**: Convert OpenAPI specs to GraphQL schemas + Strawberry resolvers
- 📝 Auto-generate complete, working Python code
- 🎨 Interactive web interface with real-time conversion
- 🛠️ Production-ready code with proper structure
- 🎯 Smart endpoint mapping based on naming conventions

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Poetry

### Option 1: Run Both Together (Recommended)

```bash
# Install all dependencies
npm run install:all

# Start both servers with one command
npm run dev
```

### Option 2: Run Separately

**Backend:**
```bash
cd backend
poetry install
poetry run python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Option 3: Use Startup Script

```bash
./start.sh
```

Backend runs at `http://localhost:8000`
Frontend runs at `http://localhost:5173`

### Run Tests

```bash
./test.sh
```

## 📖 Usage

### GraphQL → REST Example

**Input:**
```graphql
type User {
  id: ID!
  name: String!
  email: String!
}

type Query {
  user(id: ID!): User
  users: [User!]!
}

type Mutation {
  createUser(name: String!, email: String!): User!
  updateUser(id: ID!, name: String, email: String): User!
  deleteUser(id: ID!): Boolean!
}
```

**Output:**
- OpenAPI 3.0 specification
- Complete FastAPI code with routes:
  - `GET /users` → users query
  - `GET /users/{id}` → user(id) query
  - `POST /users` → createUser mutation
  - `PUT /users/{id}` → updateUser mutation
  - `DELETE /users/{id}` → deleteUser mutation

### REST → GraphQL Example

**Input:**
```json
{
  "openapi": "3.0.0",
  "paths": {
    "/users": {"get": {}},
    "/users/{id}": {"get": {}}
  }
}
```

**Output:**
- GraphQL SDL schema with Query types
- Strawberry resolver code with httpx client
- Automatic type generation

## 🧪 Testing

Sample files provided in `examples/`:
- `sample-schema.graphql` - GraphQL schema example
- `sample-openapi.json` - OpenAPI spec example

Copy and paste into the UI to test conversions.

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- graphql-core - GraphQL schema parsing
- Poetry - Dependency management
- Pre-commit hooks: Black, Ruff, Mypy, Bandit

**Frontend:**
- React + TypeScript
- Vite - Fast build tool
- Husky + lint-staged - Git hooks
- ESLint + Prettier - Code quality

## 📁 Project Structure

```
api-converter/
├── backend/
│   ├── main.py                    # FastAPI server
│   ├── converters/
│   │   ├── gql_to_rest.py        # GraphQL → REST converter
│   │   └── rest_to_gql.py        # REST → GraphQL converter
│   ├── pyproject.toml            # Poetry config + tool settings
│   └── .pre-commit-config.yaml   # Pre-commit hooks
├── frontend/
│   ├── src/
│   │   ├── App.tsx               # Main UI component
│   │   └── main.tsx
│   └── package.json
├── examples/                      # Sample schemas for testing
├── .husky/                        # Git hooks
├── test.sh                        # Automated tests
└── README.md
```

## 🔧 Development

### Backend Commands

```bash
# Install dependencies
poetry install

# Run server
poetry run python main.py

# Format code
poetry run black .

# Lint
poetry run ruff check --fix .

# Type check
poetry run mypy .

# Security check
poetry run bandit -r .

# Run all pre-commit hooks
poetry run pre-commit run --all-files
```

### Frontend Commands

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Format code
npm run format

# Lint
npm run lint
```

## 🎯 What Makes This Unique

- **Bi-directional conversion** - Most tools only go one way
- **Production-ready code** - Not just specs, but actual working implementations
- **Smart mapping** - Understands REST conventions (createX → POST, updateX → PUT, deleteX → DELETE)
- **Type preservation** - Maintains type information across conversions
- **Clean architecture** - Separation of concerns, modular design

## 🤝 Contributing

This is a learning project built to understand API design patterns and code generation techniques.

## 📝 License

MIT

---

Built with ☕ and curiosity about API design patterns.
