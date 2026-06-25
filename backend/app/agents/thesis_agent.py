from app.agents.state import AgentState
from app.tools.browser_tool import run_browser_task

async def thesis_node(state: AgentState) -> dict:
    """
    The Thesis Specialist Agent.
    It reads the state, browses the web for thesis info, and returns the updated state.
    """
    # 1. Add a log so the React frontend can show what's happening
    state.agent_logs.append("🎓 Thesis Advisor: Launching secure browser to scan faculty notice boards...")
    
    # 2. Give the browser specific guardrails for Stuttgart
    browser_instruction = (
        f"Go to the University of Stuttgart website (uni-stuttgart.de) or specific faculty sub-domains "
        f"(like f05.uni-stuttgart.de for Computer Science). The user is asking: '{state.user_prompt}'. "
        f"Find the specific thesis guidelines, templates, or open topics they are asking about. "
        f"Extract the exact details, URLs, and any professor contact info."
    )
    
    # 3. Fire the autonomous browser tool!
    extracted_data = await run_browser_task(browser_instruction)
    
    # 4. Update the state with the raw data found
    state.raw_crawled_data = extracted_data
    state.agent_logs.append("🎓 Thesis Advisor: Successfully extracted raw data. Handing back to Manager.")
    
    # 5. Tell the system to route this back to the manager for final formatting
    state.current_specialist = "manager"
    
    # Return the updated fields as a dictionary (this is how LangGraph updates the state)
    return {
        "raw_crawled_data": state.raw_crawled_data,
        "agent_logs": state.agent_logs,
        "current_specialist": state.current_specialist
    }