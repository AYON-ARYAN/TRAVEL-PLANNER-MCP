import os
import asyncio
import nest_asyncio
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_react_agent, AgentExecutor
from langchain import prompts
nest_asyncio.apply()
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

st.set_page_config(page_title="AI Travel Planner", page_icon="🌍")
st.title("🌍 AI Travel Planner Agent")
st.write("Powered by Groq + MCP (Flights, Hotels, Weather)")

# -------- AGENT FUNCTION --------
async def run_travel_agent(user_query):

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",   # best free model
        groq_api_key=GROQ_API_KEY,
        temperature=0.3
    )

    # MCP (real-time travel tools)
    mcp_config = {
        "serpapi": {
            "transport": "sse",
            "url": f"https://mcp.serpapi.com/{SERPAPI_KEY}/mcp"
        }
    }

    tools = []

    # Try MCP tools
    try:
        client = MultiServerMCPClient(mcp_config)
        tools = await asyncio.wait_for(client.get_tools(), timeout=10)
        print("MCP tools loaded")
    except:
        print("MCP slow → using LLM fallback")

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=15,
        max_execution_time=120
    )

    final_prompt = f"""
    {user_query}

    Create complete travel plan:

    1. Cultural & historical significance
    2. Current weather + forecast
    3. Best travel dates
    4. Flight options with approx prices
    5. Hotel options
    6. Day-wise itinerary
    """

    result = await agent_executor.ainvoke({"input": final_prompt})
    return result["output"]

# -------- UI --------
user_input = st.text_input(
    "Enter travel prompt:",
    "Plan a 3-day trip to Tokyo in May"
)

if st.button("Generate Travel Plan ✈️"):

    if not GROQ_API_KEY or not SERPAPI_KEY:
        st.error("Add GROQ_API_KEY and SERPAPI_API_KEY in .env")
    else:
        loop = asyncio.get_event_loop()

        with st.spinner("🤖 AI Agent planning your trip..."):
            try:
                result = loop.run_until_complete(run_travel_agent(user_input))
                st.success("Trip Generated Successfully!")
                st.markdown("## 🌍 Your Travel Plan")
                st.write(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")
