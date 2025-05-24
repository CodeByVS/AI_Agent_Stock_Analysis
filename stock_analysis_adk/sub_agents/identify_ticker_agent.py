# sub_agents/identify_ticker_agent.py

# This file defines a specialized sub-agent responsible for identifying stock tickers
# from user queries. It's a component of the Google ADK-based multi-agent system.

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
# --- Ticker Extraction Logic ---
# The core function that this agent uses to perform its task.
# In a production system, this could involve more sophisticated NLP, regex, 
# a dedicated lookup table/API, or even another LLM call for entity extraction.

def extract_ticker_from_query(query: str) -> dict:
    """Parses a natural language query to identify a stock ticker symbol.

    This function provides a basic implementation for demonstration purposes.
    It uses simple keyword matching. For a real-world application, this would need
    to be significantly more robust, potentially using NLP libraries, fuzzy matching,
    or an external service for company name to ticker symbol resolution.

    Args:
        query (str): The user's natural language query (e.g., "What's the price of Tesla stock?").

    Returns:
        dict: A dictionary with the following structure:
              {'status': 'success', 'ticker': 'TSLA'} if a ticker is found.
              {'status': 'error', 'error_message': 'Details...'} if no ticker is found or an error occurs.
    """
    # Convert query to lowercase for case-insensitive matching.
    query_lower = query.lower()
    # Predefined mapping of common company names/keywords to ticker symbols.
    # This is a simplified approach. A more scalable solution would use a database or API.
    ticker_map = {
        "tesla": "TSLA",
        "palantir": "PLTR",
        "nvidia": "NVDA",
        "nvda": "NVDA", # Allow direct ticker mention
        "apple": "AAPL",
        "aapl": "AAPL",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "googl": "GOOGL",
        "microsoft": "MSFT",
        "msft": "MSFT",
        "amazon": "AMZN",
        "amzn": "AMZN"
        # Add more mappings as needed
    }

    # Iterate through the map to find a match.
    # This could be improved with regex for more flexible matching (e.g., whole word matching).
    for keyword, ticker in ticker_map.items():
        if keyword in query_lower:
            return {"status": "success", "ticker": ticker}
    
    # If no known keyword is found, return an error.
    # A more advanced implementation might try to use an LLM to extract the company name
    # and then another tool to find its ticker symbol, or use fuzzy matching.
    return {"status": "error", "error_message": f"Could not identify a known stock ticker in the query: '{query}'. Consider using common company names or ticker symbols."}

# Wrap the Python function `extract_ticker_from_query` as a FunctionTool.
# This makes the function callable by ADK agents.
identify_ticker_tool = FunctionTool(
    fn=extract_ticker_from_query, # The function to be wrapped.
    name="extract_ticker_from_query_tool", # Explicit name for the tool.
    description="Extracts a stock ticker symbol from a given text query. Input is the query string." # Description for the LLM.
)

# --- Agent Definition ---
# Define the ADK Agent that uses the `identify_ticker_tool`.

identify_ticker_agent = Agent(
    name="identify_ticker_sub_agent", # Unique name for this sub-agent.
    model="gemini-1.5-flash",      # Specifies the LLM. Can be a smaller/faster model for focused tasks like this.
    description="A specialized sub-agent that identifies stock ticker symbols from user queries.",
    instruction=(
        "You are an expert financial assistant specialized in identifying stock ticker symbols. "
        "Given a user's query, your sole task is to use the 'extract_ticker_from_query_tool' "
        "to find the corresponding stock ticker. "
        "If the tool successfully identifies a ticker, you should output the result from the tool directly. "
        "If the tool reports an error (e.g., ticker not found), you should relay this error information. "
        "Do not attempt to answer other questions or perform other tasks."
    ),
    tools=[
        identify_ticker_tool # The tool this agent is equipped with.
    ],
    # enable_dynamic_routing=False, # Typically False for specialized agents that use a specific tool.
                                  # The orchestrator agent would handle broader routing.
)

