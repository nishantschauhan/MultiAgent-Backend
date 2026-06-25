from app.agents.state import AgentState
from app.tools.browser_tool import run_browser_task

async def admin_node(state: AgentState) -> dict:
    """
    The Admin Specialist Agent.
    Handles general university rules, deadlines, and faculty/department lists.
    """
    state.agent_logs.append("🏛️ Admin Specialist: Launching browser node to retrieve university administration data...")
    
    # Instruct the browser to focus on administrative portals and directory pages
    browser_instruction = (
        f"Go to the University of Stuttgart website (uni-stuttgart.de). The user is asking: '{state.user_prompt}'. "
        f"Find general administrative information, semester dates, re-registration deadlines, or "
        f"official structural directories/lists of staff for the requested department. "
        f"Gather the concrete names, dates, links, or contacts."
    )
    
    # Execute the autonomous browser action
    extracted_data = await run_browser_task(browser_instruction)
    
    state.raw_crawled_data = extracted_data
    state.agent_logs.append("🏛️ Admin Specialist: Data successfully extracted. Returning state control to Manager.")
    
    state.current_specialist = "manager"
    
    return {
        "raw_crawled_data": state.raw_crawled_data,
        "agent_logs": state.agent_logs,
        "current_specialist": state.current_specialist
    }