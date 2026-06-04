# Travaira ✈️🧳
An advanced, multi-agent AI Travel Planner built using LangGraph, Streamlit, and Groq (Llama 3.3). Traviara leverages specialized AI agents to orchestrate real-time flight search, hotel discovery, and comprehensive itinerary generation with persistent conversation memory.

---

## 🏗️ Architecture & Agent Workflow

Traviara utilizes a stateful multi-agent architecture managed by **LangGraph**. Instead of a single monolithic prompt, the system breaks down travel planning into dedicated components that pass context seamlessly:

1. **Supervisor / Router Node**: Analyzes user input and routes tasks to the appropriate specialized agent or compiles the final itinerary.
2. **Flight Agent (`tools/flight_tool.py`)**: Integrates with the **AviationStack API** to check real-time flight availability and tracking information.
3. **Hotel Agent (`tools/tavily_tool.py`)**: Harnesses the **Tavily Search API** to discover optimized accommodations, lodging details, and current local pricing.
4. **Persistent Memory Layer**: Uses a **PostgreSQL Checkpointer (`PostgresSaver`)** to track conversation state and thread IDs, ensuring users can resume their planning sessions seamlessly.

---

## 🚀 Features

- **Multi-Agent Orchestration**: Dynamic routing between flight verification and hotel search modules.
- **Token-Optimized Web Scraping**: Context truncation logic to feed clean, relevant data into the LLM without exhausting token windows.
- **Stateful Memory**: Enterprise-grade conversational persistence backed by PostgreSQL.
- **Modern UI**: Clean, responsive Streamlit dashboard with real-time agent status streaming and custom styling.

---

## 🛠️ Tech Stack

- **Frontend / UI**: Streamlit
- **Agent Framework**: LangGraph, LangChain Core
- **LLM Engine**: Groq Cloud (Llama 3.3)
- **Database (Checkpointing)**: PostgreSQL (`psycopg3`)
- **Data Integrations**: Tavily API, AviationStack API

---

## 📂 Project Structure

```text
├── .gitignore               # Excludes virtual environments, cache, and secrets
├── README.md                # Project documentation
├── app.py                   # Streamlit web application interface
├── main.py                  # LangGraph workflow definition & database connection
├── requirements.txt         # Production python dependencies
└── tools/
    ├── flight_tool.py       # AviationStack API flight search wrapper
    └── tavily_tool.py       # Tavily API web search engine wrapper

```

---

## 💻 Local Setup Instructions

### 1. Clone the Repository

```bash
https://github.com/lakshyawardhansinghrathore/Travaira
cd Travaira

```

### 2. Configure Your Virtual Environment

```bash
# Create environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and populate it with your respective keys:

```env
DATABASE_URL="postgresql://<username>:<password>@<host>:<port>/<dbname>"
GROQ_API_KEY="gsk_..."
TAVILY_API_KEY="tvly_..."
AVIATIONSTACK_API_KEY="your_api_key_here"

```

### 5. Run the Application Local Execution

```bash
streamlit run app.py

```

---
