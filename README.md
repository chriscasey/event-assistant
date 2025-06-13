# Event Assistant

An AI-powered event assistant that provides intelligent responses to questions about conference schedules, speakers, and venues using OpenAI's function calling with MCP (Model Context Protocol) integration.

## ✨ Features

🤖 **AI-Powered Responses** - Uses OpenAI GPT-3.5-turbo with automatic function calling  
📅 **Event Management** - Query event schedules, times, and locations  
🎤 **Speaker Information** - Get detailed speaker biographies  
🏢 **Venue Details** - Information about conference locations and facilities  
⚡ **MCP Integration** - Automatic tool discovery and schema generation  
🔍 **Natural Language** - Ask questions like "Who's speaking at 2pm?" or "Tell me about the Innovation Lab"

## 🚀 Quick Start

### 1. Setup Environment

```bash
git clone <your-repo>
cd event-assistant

# Copy environment template and add your OpenAI API key
cp env.template .env
# Edit .env: OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Build and Start

```bash
# Build and start server + database
docker compose up --build
```

### 3. Use the Assistant

**In a new terminal:**
```bash
# Start interactive client
docker compose run --rm app-client
```

**Example questions:**
```
> Who are the speakers?
> What's happening at 10:00?
> Tell me about the Main Auditorium
> What AI-related events are there?
> Show me the schedule
```

## 🏗️ Architecture

**Modern AI-First Design:**
- **Client** - Interactive terminal for natural language queries
- **Server** - FastAPI with OpenAI integration + MCP tool discovery
- **Database** - PostgreSQL with realistic conference data
- **MCP** - Automatic function registration and schema generation

### MCP Integration Benefits

✅ **Auto-Discovery** - Functions automatically registered as AI tools  
✅ **Schema Generation** - Type hints become OpenAI function schemas  
✅ **Single Source of Truth** - Function definitions in one place  
✅ **Clean Architecture** - No manual tool definitions needed  

## 📡 API

### POST `/ask`
Send natural language questions to the AI assistant.

```json
{
  "question": "Who are the speakers today?"
}
```

### GET `/health` 
Service health check endpoint.

## 🗄️ Database

**Automatically populated with realistic data:**
- **25 venues** - Main Auditorium, Innovation Lab, VR Experience Room, etc.
- **50 speakers** - Tech leaders with detailed biographies
- **100+ events** - "The Future of AI in Healthcare", "Quantum Computing", etc.

### Reset Database
```bash
docker compose down
docker volume rm event-assistant_pgdata
docker compose up --build
```

## 🛠️ Development

### Key Files

```
event-assistant/
├── client/                 # Interactive terminal client
│   ├── client.py          # Main client application
│   └── requirements.txt   # Client dependencies
├── server/                # FastAPI server + AI logic
│   ├── main.py           # FastAPI app with MCP integration
│   ├── server.py         # MCP tool definitions (@mcp.tool)
│   ├── models.py         # Database models
│   ├── db.py            # Database configuration
│   └── seed.py          # Realistic test data
├── docker-compose.yml   # Container orchestration
├── env.template        # Environment setup guide
└── .gitignore         # Security (protects API keys)
```

### MCP Tool Definition

```python
# In server/server.py
@mcp.tool()
def get_schedule() -> list:
    """Get the complete event schedule with all talks, times, locations, and speakers"""
    # Implementation automatically becomes available to AI
```

### Adding New Functions

1. **Add to `server/server.py`:**
```python
@mcp.tool()
def new_function(param: str) -> dict:
    """Description for AI to understand the function"""
    # Your implementation
    return {"result": "data"}
```

2. **That's it!** MCP automatically:
   - Registers the function as an AI tool
   - Generates OpenAI-compatible schemas
   - Makes it available for function calling

## 🔧 Commands

```bash
# Essential commands
docker compose up --build        # Start everything
docker compose run --rm app-client  # Start client
docker compose logs -f           # View logs
docker compose down              # Stop everything

# Development
docker compose logs -f app-server   # Server logs only
docker compose build              # Rebuild containers
docker volume ls                  # List volumes
```

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `DATABASE_URL` | PostgreSQL connection | No (auto-configured) |

## 🧪 Testing

**Quick API test:**
```bash
# Check health
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Who are the speakers?"}'
```

## 📋 Requirements

- **Docker & Docker Compose**
- **OpenAI API Key** (set in `.env`)
- **Internet connection** (for OpenAI API)

## 🚀 What's New

**v2.0 - MCP Integration:**
- ✅ Full MCP (Model Context Protocol) implementation
- ✅ Automatic tool discovery and registration  
- ✅ 90+ lines of code reduction (removed manual tool definitions)
- ✅ Cleaner, more maintainable architecture
- ✅ Type-safe function schemas from Python type hints
- ✅ Single source of truth for function definitions

**Code Quality:**
- ✅ Cleaned up from 300+ to ~180 lines in main files
- ✅ Removed debug logging and verbose comments
- ✅ Production-ready error handling
- ✅ Version-pinned dependencies for reproducible builds

## 🎯 Perfect For

- **Learning AI function calling** with real-world examples
- **Conference/event management** systems
- **Natural language interfaces** to databases
- **MCP integration** examples and best practices

## 📄 License

MIT License

---

**Built with FastAPI, OpenAI, MCP, PostgreSQL, and Docker** 🚀 