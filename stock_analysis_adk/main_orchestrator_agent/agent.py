# main_orchestrator_agent/agent.py

# This file defines the main orchestrator agent for the Google ADK-based stock analysis system.
# It coordinates tasks among various specialized sub-agents to process user queries about stocks.

from google.adk.agents import Agent, LlmAgent # LlmAgent provides more control if needed.
from google.adk.tools import FunctionTool # Used for wrapping Python functions as tools for agents.

# Import sub-agents. These are ADK Agents themselves and can be used as tools by other agents.
# The relative imports assume this file is part of the 'stock_analysis_adk' package.
from ..sub_agents.identify_ticker_agent import identify_ticker_agent
from ..sub_agents.ticker_news_agent import ticker_news_agent
from ..sub_agents.ticker_price_agent import ticker_price_agent
from ..sub_agents.ticker_price_change_agent import ticker_price_change_agent
from ..sub_agents.ticker_analysis_agent import ticker_analysis_agent

# Define the root orchestrator agent.
root_agent = Agent(
    name="main_orchestrator_agent", 
    model="gemini-1.5-flash",      
    description="Orchestrates stock analysis tasks by delegating to specialized sub-agents.",
    instruction=(
        "You are the main orchestrator for a stock analysis system. Your primary role is to understand "
        "the user's query about stocks, determine the sequence of analytical steps required, and then "
        "delegate these tasks to the appropriate specialized sub-agents. "
        "The available sub-agents are: identify_ticker (to find the stock symbol), "
        "ticker_news (to fetch recent news), ticker_price (to get current stock price), "
        "ticker_price_change (to calculate price fluctuations), and ticker_analysis (to synthesize insights). "
        "After gathering information from these sub-agents, you must synthesize it into a coherent and "
        "comprehensive answer for the user."
    ),
    tools=[
        # List of sub-agents that this orchestrator can use as tools.
        # ADK Agents can be seamlessly integrated as tools for other agents.
        identify_ticker_agent,
        ticker_news_agent,
        ticker_price_agent,
        ticker_price_change_agent,
        ticker_analysis_agent
    ],
   
)

