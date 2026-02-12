import os
from dotenv import load_dotenv
from langchain_classic.agents import create_react_agent, AgentExecutor

from langchain_mcp_adapters.client import MultiServerMCPClient
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
# 1. Your API Keys
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

async def get_tools():
    # In MCP, we connect to the SERVER, not the individual search URL.
    # SerpApi provides a special MCP URL that uses your API key.
    SERPAPI_MCP_URL = f"https://mcp.serpapi.com/{SERPAPI_KEY}/mcp"

    # Define the servers you are connecting to
    client = MultiServerMCPClient({
        "serpapi": {
            "transport": "sse", 
            "url": SERPAPI_MCP_URL
        },
        # If you're using a local Weather MCP server:
        "weather": {
            "transport": "stdio", 
            "command": "npx", 
            "args": ["-y", "@modelcontextprotocol/server-weather"]
        }
    })
    
    # This single line discovers ALL tools (flights, hotels, search) from the server
    tools = await client.get_tools()
    return tools