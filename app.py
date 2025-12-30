import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. UI Configuration
st.set_page_config(page_title="Max: Startup Architect", page_icon="🚀", layout="wide")
st.title("🚀 Max: Multi-Agent Startup Architect")

# 2. Setup (LLM & Tools)
load_dotenv()

# CRITICAL: Use st.secrets for Streamlit Cloud stability
groq_api_key = st.secrets["GROQ_API_KEY"]

# Using a hyper-stable configuration for Groq
my_llm = LLM(
    model="groq/llama-3.1-8b-instant", 
    api_key=groq_api_key,
    temperature=0.1,
    max_tokens=1000, # Prevents long responses that trigger 'None' errors
    provider="groq"
)

@tool("duckduckgo_search")
def search_tool(query: str):
    """Search the internet for info. Returns very short results to save tokens."""
    # Reduced to 800 characters - Groq's free tier handles this much better
    return DuckDuckGoSearchRun().run(query)[:800]

# 3. User Input
user_idea = st.text_input("What is your startup idea?", placeholder="e.g. AI for Norway travel")

if st.button("Generate Roadmap"):
    if not user_idea:
        st.warning("Please enter an idea first!")
    else:
        with st.status("🤖 AI Crew is thinking...", expanded=True) as status:
            # --- AGENTS (Ultra-minimal backstories to save tokens) ---
            researcher = Agent(
                role='Researcher',
                goal=f'Find 2 competitors for {user_idea}',
                backstory='Market analyst.',
                tools=[search_tool], 
                llm=my_llm, 
                verbose=True, 
                allow_delegation=False,
                max_iter=2 # Stops the agent from over-thinking and crashing
            )
            
            architect = Agent(
                role='Architect',
                goal=f'Suggest a tech stack for {user_idea}',
                backstory='Cloud expert.',
                llm=my_llm, 
                verbose=True, 
                allow_delegation=False,
                max_iter=2
            )

            # --- TASKS (Strict word limits to prevent API timeouts) ---
            t1 = Task(
                description=f"Identify 2 competitors for {user_idea}.", 
                agent=researcher, 
                expected_output="A bulleted list of 2 competitors."
            )
            t2 = Task(
                description="Suggest 3 key technologies for the stack.", 
                agent=architect, 
                expected_output="A tech stack list.", 
                context=[t1]
            )

            # --- CREW (Slow and steady wins the race) ---
            crew = Crew(
                agents=[researcher, architect], 
                tasks=[t1, t2], 
                process=Process.sequential, 
                max_rpm=1, # Strict 1 request per minute for Free Tier stability
                memory=False, # Memory requires OpenAI/Embeddings, keep it False
                tracing=True
            )
            
            result = crew.kickoff()
            status.update(label="✅ Success!", state="complete", expanded=False)

        # 4. Display Result
        st.subheader("Final Blueprint")
        st.markdown(result.raw)
        st.download_button("Download (.md)", result.raw, file_name="plan.md")