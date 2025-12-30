# 🚀 Max: Multi-Agent Startup Architect

An Agentic AI system that transforms raw startup ideas into comprehensive market reports and technical architectures. Built with **CrewAI** and **Groq (Llama 3.1)** for high-speed reasoning.

## 🧠 How it Works
This system utilizes two specialized AI agents:
1. **Market Research Specialist**: Scours the web using DuckDuckGo to identify competitors and market gaps.
2. **Cloud Architect**: Designs a scalable tech stack based on the researcher's findings.

## 🛠️ Tech Stack
- **Framework**: CrewAI
- **LLM**: Groq (Llama-3.1-8b-instant)
- **Frontend**: Streamlit
- **Search**: DuckDuckGo API

## ⚙️ Setup
1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Add your `GROQ_API_KEY` to a `.env` file.
5. Run the app: `streamlit run app.py`