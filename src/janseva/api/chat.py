import json
from typing import AsyncGenerator, Dict, Any
from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from janseva.agents.orchestrator import agent_graph

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

async def generate_chat_stream(message: str, session_id: str) -> AsyncGenerator[str, None]:
    """Generates an SSE stream from the LangGraph agent."""
    
    state_input = {
        "messages": [HumanMessage(content=message)],
        "language": "english",  # Can be dynamic later
        "session_id": session_id,
        "contact_number": None,
    }
    
    config = {"configurable": {"thread_id": session_id}}
    
    try:
        # Stream events from the graph
        async for event in agent_graph.astream_events(state_input, config=config, version="v1"):
            kind = event["event"]
            
            # We are interested in token streaming from the chat model
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Format as Server-Sent Event
                    data = json.dumps({"content": content})
                    yield f"data: {data}\n\n"
                    
            elif kind == "on_tool_start":
                tool_name = event["name"]
                data = json.dumps({"content": f"\n_[Using tool: {tool_name}]_\n"})
                yield f"data: {data}\n\n"

        # Signal completion
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        error_msg = json.dumps({"error": str(e)})
        yield f"data: {error_msg}\n\n"

@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    Endpoint for the web frontend to stream chat responses via SSE.
    """
    return StreamingResponse(
        generate_chat_stream(req.message, req.session_id),
        media_type="text/event-stream"
    )
