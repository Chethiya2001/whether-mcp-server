import logging
import os
import random
import sys
from dotenv import load_dotenv
import requests

from mcp.server.mcpserver import MCPServer

name = "FastMCP-server"
load_dotenv()  # Load environment variables from .env file
#Config Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(name)

#Create MCP server
port = int(os.environ.get("PORT", 8080))
mcp_server = MCPServer(name=name)

@mcp_server.tool()
def add(a:int,b:int)->int:
    """
    Adds two integers.
    """
    logger.info(f"Tool called: add({a},{b})")
    return a+b

@mcp_server.tool()
def get_secret_word()->str:
    """
    Returns a secret word.
    """
    logger.info("Tool called: get_secret_word()")
    return random.choice(["apple", "banana", "cherry", "date", "elderberry"]) 

@mcp_server.tool()
def fetch_weather_data(city:str)->str:
    """Get current weather for a city"""
    logger.info(f"Tool called: fetch_weather_data({city})")
    try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}",timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return "Error fetching weather data."


if __name__ == "__main__":
    logger.info(f"Starting {name} on port {port}")
    port = int(os.environ.get("PORT", 8080))

    try:
        mcp_server.run(transport="sse", port=port)
    except Exception as e:
        logger.info(f"Error running server: {e}")
        sys.exit(1)
    finally:
        logger.info(f"Shutting down {name}")
