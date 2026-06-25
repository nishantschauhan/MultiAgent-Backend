from app.agents.state import AgentState
from app.tools.browser_tool import run_browser_task

async def library_node(state: AgentState) -> dict:
    """
    The Library Specialist Agent.
    Dedicated exclusively to checking literature availability via Katalog plus.
    """
    state.agent_logs.append("📚 Library Catalog: Opening browser session targeting the University Library portal...")
    
    # Directly guide the browser agent to the rigid Stuttgart library search engine
    browser_instruction = (
        f"Go directly to the University of Stuttgart Library Catalog (Katalog plus) at "
        f"https://katalogplus.ub.uni-stuttgart.de/. The user wants to find information about: '{state.user_prompt}'. "
        f"Search for this item in the search bar, look at the top results, and determine if it is available, "
        f"on loan, or located at the Vaihingen or City Center campus library. Extract the book signature or location shelf."
    )
    
    extracted_data = await run_browser_task(browser_instruction)
    
    state.raw_crawled_data = extracted_data
    state.agent_logs.append("📚 Library Catalog: Availability tracked successfully. Handing back to Manager.")
    
    state.current_specialist = "manager"
    
    return {
        "raw_crawled_data": state.raw_crawled_data,
        "agent_logs": state.agent_logs,
        "current_specialist": state.current_specialist
    }