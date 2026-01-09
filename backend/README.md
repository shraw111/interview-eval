# Interview Agent Backend

FastAPI backend for the Interview Agent evaluation system.

## Features

- **REST API**: Create and manage evaluations
- **WebSocket**: Real-time progress streaming
- **LangGraph Integration**: Reuses existing evaluation engine from `src/graph/`

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

The backend uses the same `.env` file as the main project. Make sure you have:

```bash
# In project root/.env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
```

### 3. Run the Server

```bash
cd backend
python run.py
```

The server will start on `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### REST API

- `POST /api/v1/evaluations` - Create new evaluation
- `GET /api/v1/evaluations/{id}` - Get evaluation status/results
- `GET /api/v1/evaluations` - List all evaluations (paginated)
- `GET /api/v1/health` - Health check

### WebSocket

- `ws://localhost:8000/ws/evaluations/{evaluation_id}` - Real-time progress stream

## WebSocket Events

The WebSocket sends the following events:

```json
// Connected
{ "type": "connected", "evaluation_id": "...", "timestamp": "..." }

// Evaluation started
{ "type": "evaluation_started", "evaluation_id": "...", "timestamp": "..." }

// Node started (0%, 25%, 50%, 75%)
{ "type": "node_started", "node": "primary_evaluator", "progress_percentage": 0, "timestamp": "..." }

// Node completed (25%, 50%, 75%, 100%)
{
  "type": "node_completed",
  "node": "primary_evaluator",
  "progress_percentage": 25,
  "tokens": { "input": 1234, "output": 567 },
  "output_preview": "First 200 chars...",
  "timestamp": "..."
}

// Evaluation completed
{ "type": "evaluation_completed", "evaluation_id": "...", "result": {...}, "timestamp": "..." }

// Error
{ "type": "error", "error": "Error message", "node": "...", "timestamp": "..." }
```

## Testing

### Test with curl

```bash
# Create evaluation
curl -X POST http://localhost:8000/api/v1/evaluations \
  -H "Content-Type: application/json" \
  -d @test_request.json

# Get evaluation
curl http://localhost:8000/api/v1/evaluations/{evaluation_id}

# Health check
curl http://localhost:8000/api/v1/health
```

### Test WebSocket

Use a WebSocket client like `wscat`:

```bash
npm install -g wscat
wscat -c "ws://localhost:8000/ws/evaluations/{evaluation_id}"
```

## Architecture

```
backend/
├── app/
│   ├── main.py                      # FastAPI app entry
│   ├── models/
│   │   ├── requests.py              # Pydantic request schemas
│   │   ├── responses.py             # Pydantic response schemas
│   │   └── events.py                # WebSocket event schemas
│   ├── services/
│   │   ├── evaluation_service.py    # Core evaluation logic
│   │   └── storage_service.py       # In-memory storage
│   ├── api/
│   │   ├── routes/
│   │   │   ├── evaluations.py       # REST endpoints
│   │   │   └── health.py            # Health check
│   │   └── websocket/
│   │       ├── manager.py           # WebSocket connection manager
│   │       └── evaluation_stream.py # WebSocket endpoint
│   └── utils/
│       └── graph_executor.py        # LangGraph wrapper
└── run.py                           # Server runner
```

## Integration with Existing Code

The backend **reuses** all existing LangGraph code from `src/`:

- `src/graph/graph.py` - LangGraph workflow (imported directly)
- `src/graph/nodes.py` - 4-agent implementations (unchanged)
- `src/utils/azure_client.py` - Azure OpenAI client (unchanged)
- `src/prompts/manager.py` - Prompt versioning (unchanged)

No modifications to the existing evaluation logic are needed!
