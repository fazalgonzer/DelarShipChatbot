
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from typing import Dict, List, Any, AsyncGenerator
from llm import llmWithTools
from tools.weather import get_weather
from tools.check_appointment_availability import check_appointment_availability
from tools.get_dealership_address import get_dealership_address
from tools.schedule_appointment import schedule_appointment

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Map tool names to functions
TOOL_MAPPING = {
    "get_weather": get_weather,
    "check_appointment_availability": check_appointment_availability,
    "get_dealership_address": get_dealership_address,
    "schedule_appointment": schedule_appointment
}

class QueryRequest(BaseModel):
    query: str
    session_id: str

async def generate_assistant_response(query: str) -> AsyncGenerator[Dict[str, Any], None]:
    # Start the response
    try:
        yield {"event": "chunk", "data": "Processing your question... Please wait.\n"}
        await asyncio.sleep(1)
        res=llmWithTools.invoke(query)
        if res.tool_calls:
            # If there are tool calls, process them
            for tool_call in res.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                if tool_name in TOOL_MAPPING:
                    tool_msg = TOOL_MAPPING[tool_name].invoke(tool_args)  # Invoke the corresponding function
                    
                    # Ensure JSON formatting for frontend
                    yield {
                        "event": "tool_output",
                        "data": json.dumps({"name": tool_name, "output": json.dumps(tool_msg['output'])}, ensure_ascii=False)
                    }
                    await asyncio.sleep(0.5)
                else:
                    yield {
                        "event": "error",
                        "data": json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)
                    }
            
        
                
        else:
            # If no tool calls, simulate a response from the assistant
            yield {"event": "chunk", "data": res.content}
            await asyncio.sleep(1)

      

        
        # End the response stream
        yield {"event": "end", "data": ""}
    except Exception as e:
        yield {"event": "error", "data": f"An error occurred: {str(e)}"}

@app.post("/query")
async def query_endpoint(payload: QueryRequest):
    return EventSourceResponse(generate_assistant_response(payload.query))

