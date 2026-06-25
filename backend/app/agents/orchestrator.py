import os
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from app.agents.state import AgentState

# Define the structure for the routing decision
class RouteDecision(BaseModel):
    target_specialist: str = Field(description="Must be exactly: 'admin', 'thesis', or 'library'.")
    reasoning: str = Field(description="Brief reason why this specialist was chosen.")

async def manager_node(state: AgentState) -> dict:
    """
    The Main Orchestrator.
    Routes initial requests, and compiles final answers once data is gathered.
    """
    # Initialize Google Gemini LLM connection
    # gemini-1.5-flash is extremely fast and perfect for quick routing/formatting
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # ---------------------------------------------------------
    # SCENARIO A: A sub-agent has returned with raw web data
    # ---------------------------------------------------------
    if state.raw_crawled_data is not None:
        state.agent_logs.append("🧠 Manager: Reviewing scraped data and formatting final response...")
        
        prompt = (
            f"The user asked: '{state.user_prompt}'\n\n"
            f"The specialist agent found this raw data on the web:\n{state.raw_crawled_data}\n\n"
            f"Write a clean, professional, and helpful markdown response to the user based ONLY on this data. "
            f"Do not make up facts."
        )
        
        response = await llm.ainvoke(prompt)
        
        state.final_compiled_answer = response.content
        state.agent_logs.append("✅ Manager: Final response compiled. Task complete.")
        state.current_specialist = "done"  # Signal to stop the loop
        
        return {
            "final_compiled_answer": state.final_compiled_answer,
            "agent_logs": state.agent_logs,
            "current_specialist": state.current_specialist
        }

    # ---------------------------------------------------------
    # SCENARIO B: This is a brand new user request. Route it!
    # ---------------------------------------------------------
    state.agent_logs.append("🧠 Manager: Analyzing user intent to determine the best specialist...")
    
    structured_llm = llm.with_structured_output(RouteDecision)
    system_prompt = (
        "You are the routing manager for the Uni Stuttgart AI Copilot. "
        "Read the user's request and assign it to the correct specialist:\n"
        "- 'admin': For general university rules, semester dates, faculty directories, or IT setup.\n"
        "- 'thesis': For thesis topics, guidelines, master/bachelor templates, or specific institute boards.\n"
        "- 'library': For checking book availability, physical catalog searches, or literature."
    )
    
    decision = await structured_llm.ainvoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state.user_prompt}
    ])
    
    state.current_specialist = decision.target_specialist
    state.routing_reasoning = decision.reasoning
    state.agent_logs.append(f"🧠 Manager: Routing request to the '{decision.target_specialist}' agent. Reason: {decision.reasoning}")
    
    return {
        "current_specialist": state.current_specialist,
        "routing_reasoning": state.routing_reasoning,
        "agent_logs": state.agent_logs
    }