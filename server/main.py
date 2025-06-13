from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from openai import OpenAI

# Import the MCP server and functions
from server import mcp, get_schedule, get_talk_by_time, get_location, get_speaker_info
from db import init_db

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
init_db()

app = FastAPI(title="Event Assistant API")

@app.on_event("startup")
async def startup_event():
    """Seed the database with initial data if it's empty"""
    try:
        schedule = get_schedule()
        if not schedule:
            import subprocess
            import os
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            seed_path = os.path.join(current_dir, "seed.py")
            
            result = subprocess.run(["python", seed_path], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error running seed script: {result.stderr}")
    except Exception as e:
        print(f"Error during startup: {e}")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

# Function mapping for direct calls
FUNCTION_MAP = {
    "get_schedule": get_schedule,
    "get_talk_by_time": get_talk_by_time,
    "get_location": get_location,
    "get_speaker_info": get_speaker_info
}

async def get_mcp_tools():
    """Get tool definitions from MCP server"""
    try:
        tools_response = await mcp.list_tools()
        tools = []
        
        for tool in tools_response.tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema or {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            tools.append(openai_tool)
        
        return tools
    except Exception as e:
        # Fallback to basic tool definitions if MCP fails
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_schedule",
                    "description": "Get the complete event schedule with all talks, times, locations, and speakers",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_talk_by_time",
                    "description": "Find a specific event/talk happening at a given time",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "time": {"type": "string", "description": "The time to search for (e.g., '10:00', '14:30')"}
                        },
                        "required": ["time"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_location",
                    "description": "Get information about a specific venue or location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "The name of the location/venue"}
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_speaker_info",
                    "description": "Get biographical information about a specific speaker",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "The name of the speaker"}
                        },
                        "required": ["name"]
                    }
                }
            }
        ]

def call_function(name: str, arguments: dict) -> str:
    """Execute function calls directly"""
    try:
        if name in FUNCTION_MAP:
            result = FUNCTION_MAP[name](**arguments)
            return json.dumps(result) if isinstance(result, (dict, list)) else str(result)
        else:
            return f"Unknown function: {name}"
    except Exception as e:
        return f"Error calling {name}: {str(e)}"

async def process_with_ai(question: str) -> str:
    """Process question using AI with function tools"""
    
    if question.lower() == "ping":
        return "Server is ready!"
    
    try:
        if not os.getenv("OPENAI_API_KEY"):
            return "AI assistant is not configured. Please set OPENAI_API_KEY environment variable."
        
        # Get tools (try MCP first, fallback to manual definitions)
        tools = await get_mcp_tools()
        
        messages = [
            {
                "role": "system",
                "content": """You are an intelligent event assistant with access to a conference database. 

Use the available tools to answer questions about events, speakers, schedules, and venues. Always call the appropriate tools rather than guessing."""
            },
            {
                "role": "user",
                "content": question
            }
        ]
        
        # Get response from OpenAI with tools
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            messages.append(response_message)
            
            # Execute tool calls
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_response = call_function(function_name, function_args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_response
                })
            
            # Get final response
            final_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            return final_response.choices[0].message.content
        else:
            return response_message.content
            
    except Exception as e:
        return f"Sorry, I encountered an error while processing your question: {str(e)}"

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """Main endpoint for asking questions to the event assistant using AI"""
    try:
        answer = await process_with_ai(request.question)
        return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 