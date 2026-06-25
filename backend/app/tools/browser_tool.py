import os
import sys
import asyncio
from threading import Thread
from dotenv import load_dotenv

# We only need Agent and Browser now!
from browser_use import Agent, Browser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# --- GOOGLE MODEL PATCHES ---
# Bypasses the missing attribute errors for browser-use
ChatGoogleGenerativeAI.provider = "google"
ChatGoogleGenerativeAI.model_name = property(lambda self: self.model)
# ----------------------------

def _run_agent_in_thread(task_description: str, result_container: list):
    """
    Runs the browser in a completely isolated thread.
    This guarantees Uvicorn cannot block the Chromium window from opening on Windows.
    """
    try:
        # Force Windows to use the correct architecture for THIS specific thread
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # Create a fresh, uncontaminated event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def main():
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash", 
                api_key=os.getenv("GOOGLE_API_KEY")
            )
            
            # --- THE INVISIBLE BROWSER FIX ---
            # In the newest package update, we just pass headless directly!
            browser = Browser(headless=True)
            # ---------------------------------
            
            agent = Agent(
                task=task_description, 
                llm=llm,
                browser=browser
            )
            
            history = await agent.run()
            
            # Clean up the hidden browser when finished
            await browser.close()
            
            return history.final_result()

        # Execute and save the result back to the main program
        result_container[0] = loop.run_until_complete(main())
        loop.close()
        
    except Exception as e:
        result_container[0] = f"Browser Error: {str(e)}"


async def run_browser_task(task_description: str) -> str:
    """
    Launches an autonomous browser to search the web based on a natural language task.
    """
    try:
        result = [None]
        
        thread = Thread(target=_run_agent_in_thread, args=(task_description, result))
        thread.start()
        
        while thread.is_alive():
            await asyncio.sleep(0.5)
            
        if result[0] and "Browser Error:" in result[0]:
            print(f"\n🚨 BROWSER CRASH: {result[0]}\n")
            
        return result[0]

    except Exception as e:
        print(f"\n🚨 BROWSER CRASH REASON: {str(e)}\n")
        return f"Browser tool encountered an error while navigating: {str(e)}"