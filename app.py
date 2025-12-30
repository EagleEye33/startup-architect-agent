import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# 1. UI Configuration
st.set_page_config(page_title="Max: Startup Architect", page_icon="🚀", layout="wide")
st.title("🚀 Max: Multi-Agent Startup Architect")
st.markdown("Enter your idea below, and our AI crew will build a market and tech roadmap for you.")

# 2. Setup (LLM & Tools)
load_dotenv()
my_llm = LLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"),temperature=0.1,provider="groq")

@tool("duckduckgo_search")
def search_tool(query: str):
    """Search the internet for information."""
    return DuckDuckGoSearchRun().run(query)[:2000]

# 3. User Input
user_idea = st.text_input("What is your startup idea?", placeholder="e.g. A robotic chef for small apartments")

if st.button("Generate Roadmap"):
    if not user_idea:
        st.warning("Please enter an idea first!")
    else:
        with st.status("🤖 Agents are working...", expanded=True) as status:
            # --- AGENTS ---
            researcher = Agent(
                role='Market Specialist',
                goal=f'Find 3 competitors and gaps for {user_idea}',
                backstory='Expert in tech market analysis.',
                tools=[search_tool], llm=my_llm, verbose=True, allow_delegation=False,max_iterations=3
            )
            
            architect = Agent(
                role='Cloud Architect',
                goal=f'Design a tech stack for {user_idea}',
                backstory='Expert in AWS and Docker.',
                llm=my_llm, verbose=True, allow_delegation=False
            )

            # --- TASKS ---
            t1 = Task(description=f"Research {user_idea}", agent=researcher, expected_output="A summary of 3 competitors and 2 market trends (max 400 words).")
            t2 = Task(description="Technical design.", agent=architect, expected_output="Tech stack.", context=[t1])

            # --- CREW ---
            crew = Crew(agents=[researcher, architect], tasks=[t1, t2], process=Process.sequential, manager_llm=my_llm, verbose=True,max_rpm=3, tracing=True, memory=False)
            
            st.write("🕵️ Researcher is searching the web...")
            result = crew.kickoff()
            status.update(label="✅ Roadmap Complete!", state="complete", expanded=False)

        # 4. Display Result
        st.subheader("Your Startup Blueprint")
        st.markdown(result.raw)
        
        # Add a download button for the professional touch
        st.download_button("Download Report (.md)", result.raw, file_name="startup_plan.md")