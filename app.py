import os
import asyncio
import nest_asyncio
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

nest_asyncio.apply()
load_dotenv()

# API KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="AI Travel Planner", page_icon="🌍")
st.title("🌍 AI Travel Planner Agent")
st.write("Plan trips with AI (Flights, Hotels, Weather, Itinerary)")

# -------- AGENT FUNCTION --------
async def run_travel_agent(user_query):

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=GROQ_API_KEY,
        temperature=0.3
    )

    prompt = f"""
You are a professional AI travel planner.

User request:
{user_query}

Create a COMPLETE travel plan with:

1. Cultural & historical significance of place
2. Current weather & expected weather
3. Best travel dates
4. Flight options with approx price
5. Hotel options with price range
6. Day-wise itinerary

Return nicely formatted answer.
"""

    response = llm.invoke(prompt)
    return response.content

# -------- UI --------
user_input = st.text_input(
    "Enter travel prompt:",
    "Plan a 3-day trip to Tokyo in May"
)

if st.button("Generate Travel Plan ✈️"):

    if not GROQ_API_KEY:
        st.error("Add GROQ_API_KEY in Streamlit secrets")
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
