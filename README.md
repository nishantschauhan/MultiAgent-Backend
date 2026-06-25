# Multi-Agent Autonomous Browser Backend

An advanced multi-agent system built with Python, FastAPI, and LangChain that orchestrates autonomous agents to perform complex, multi-step web browsing and information retrieval tasks. Utilizing `browser-use`, the backend can spin up headless browser sessions to navigate, read, and extract information from websites dynamically, providing a seamless "chat-with-AI" experience.

---

## 🚀 Features

* **Orchestration Architecture:** An admin/manager node structure that handles incoming natural language tasks and routes them efficiently.
* **Autonomous Browser Agent:** Uses the modern `browser-use` library integrated with Gemini LLMs to browse real websites actively.
* **Seamless Headless Execution:** Runs standard browser windows silently in the background (`headless=True`) to deliver clean, chat-focused responses without screen interruption.
* **Async Thread Isolation:** Runs the automated browser loops inside an isolated thread to ensure the async event loop never blocks the main FastAPI/Uvicorn server, ensuring high responsiveness.
* **Tailored for Windows Platforms:** Configured explicitly with the Windows Proactor event loop policy to guarantee seamless subprocess execution on Windows environments.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python 3.13+)
* **Server:** Uvicorn (with hot-reloading for development)
* **LLM Orchestration:** LangChain (`langchain-core`, `langchain-google-genai`)
* **Core Intelligence:** Google Gemini (`gemini-2.5-flash` / `gemini-2.5-pro`)
* **Automation:** `browser-use` (Playwright-backed autonomous agent navigation)

---

## 📋 Prerequisites

Before setting up the project, ensure your machine has the following installed:
* [Python 3.11+](https://www.python.org/downloads/) (Python 3.13 recommended)
* [Git](https://git-scm.com/)
* A Google AI Studio API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

---

## ⚙️ Installation & Setup

Follow these step-by-step instructions to get your development environment running locally.

### 1. Navigate to the Backend Directory
Open your terminal (e.g., Git Bash) and go to your backend folder:
```bash
cd ~/OneDrive/Desktop/MultiAgent/backend


2. Set Up a Virtual Environment
Create an isolated virtual environment to manage dependencies securely:

Bash
python -m venv venv
3. Activate the Virtual Environment
On Windows (Git Bash / Command Prompt):

Bash
source venv/Scripts/activate
On macOS/Linux:

Bash
source venv/bin/activate
When successfully activated, your terminal prompt will show (venv) at the beginning.

4. Install Dependencies
Ensure your environment has all the vital packages required for the agent ecosystem:

Bash
pip install fastapi uvicorn langchain-core langchain-google-genai browser-use python-dotenv
5. Install Browser Automation Drivers
Since browser-use drives a physical browser instance behind the scenes, initialize Playwright's required binaries:

Bash
playwright install
🔑 Environment Variables Setup
The system relies on a secure environment file to handle API authentication keys safely without committing them to version control.

Create a file named .env inside the backend/ directory.

Open the .env file and add your Google API key:

Code snippet
GOOGLE_API_KEY=your_actual_gemini_api_key_here
⚠️ Security Warning: Never commit your .env file to public GitHub repositories. Ensure it is explicitly included in your .gitignore file.

🖥️ Running the Application
Once your virtual environment is active and variables are populated, start up the FastAPI local development server using Uvicorn:

Bash
uvicorn app.main:app --reload
Understanding the Terminal Logs:
Will watch for changes... indicates that the --reload hot-reloading flag is working. The server will automatically restart whenever you save file updates.

Once initialized, the backend will listen for requests at: http://127.0.0.1:8000

🔍 API Endpoints Quick Reference
POST /api/agent/search
Dispatches a text payload task to the orchestrator agent node.

Request Body JSON Structure:

JSON
{
  "task_description": "Who is Katrin Schneider at University of Stuttgart?"
}
Expected Behavior: The manager receives the payload, assigns it to the browser_tool, launches a hidden browser session to evaluate the site elements, finds the target parameters, and returns a plain markdown-formatted textual response safely inside the chat window payload.

🛠️ Troubleshooting & Quotas
429 RESOURCE_EXHAUSTED Error: The free-tier Gemini API key allows up to 15 Requests Per Minute (RPM). Because an autonomous browser loop makes quick, rapid calls to calculate its next UI clicks, you might hit the rate limit. If this occurs, wait 60 seconds for your window to reset or upgrade to a pay-as-you-go billing profile on Google AI Studio.

Speed Optimization: If the processing workflow feels slow, verify your browser_tool.py is configured to run gemini-2.5-flash rather than the larger, resource-heavy gemini-2.5-pro architecture.
