from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import asyncio

# Import your State and Agents
from app.agents.state import AgentState
from app.agents.orchestrator import manager_node
from app.agents.admin_agent import admin_node
from app.agents.thesis_agent import thesis_node
from app.agents.library_agent import library_node

# --- THE WINDOWS ASYNC SUBPROCESS FIX ---
# Force Windows to use the Proactor loop architecture so it can spawn the browser window
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
# ----------------------------------------

from fastapi import FastAPI
# ... the rest of your existing imports and FastAPI code ...

app = FastAPI(title="Multiagent Academic Copilot Backend")

# Configure CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the incoming request from React looks like
class SearchRequest(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return {"status": "online", "message": "Multiagent Backend is running."}

@app.post("/api/agent/search")
async def run_agent_system(request: SearchRequest):
    """
    The Core Multi-Agent Execution Loop.
    React hits this endpoint, and this loop runs until the agents find the answer.
    """
    # 1. Initialize the shared notebook (State) with the user's prompt
    state = AgentState(user_prompt=request.message)

    # 2. The Execution Loop
    # It starts at "manager" by default. It will loop, passing control between 
    # the manager and specialists until the manager sets it to "done".
    while state.current_specialist != "done":
        
        if state.current_specialist == "manager":
            await manager_node(state)
            
        elif state.current_specialist == "admin":
            await admin_node(state)
            
        elif state.current_specialist == "thesis":
            await thesis_node(state)
            
        elif state.current_specialist == "library":
            await library_node(state)
            
        else:
            # Safety break if an unknown specialist is assigned
            break 

    # 3. Return the final compiled answer and the execution logs back to React
    return {
        "reply": state.final_compiled_answer,
        "logs": state.agent_logs
    }