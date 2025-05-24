# sub_agents/ticker_news_agent.py

# This file defines a specialized sub-agent for fetching recent news articles 
# related to a specific stock ticker. It utilizes the Alpha Vantage API.

import os
import requests
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv # To manage API keys and other environment variables.

# --- Environment Variable Loading ---
# Load environment variables, primarily the ALPHA_VANTAGE_API_KEY.
# It attempts to load from a .env file located at the project root first.
# This setup assumes the .env file is in `c:\Project\Intership_Test_AI_Agent\.env`.

# Construct the path to the root .env file relative to this script's location.
# __file__ -> sub_agents/ticker_news_agent.py
# os.path.dirname(__file__) -> sub_agents
# os.path.join(..., '..') -> stock_analysis_adk
# os.path.join(..., '..', '..') -> c:\Project\Intership_Test_AI_Agent (project root)
project_root_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

if os.path.exists(project_root_env_path):
    load_dotenv(dotenv_path=project_root_env_path)

else:
    # Fallback: try loading .env from the current working directory if the root one isn't found.
    # This might be relevant if the script is run from a different context.
    if not load_dotenv():
        print(f"Warning: .env file not found at {project_root_env_path} or current working directory. ALPHA_VANTAGE_API_KEY might not be set.")


# Retrieve the API key and set the base URL for Alpha Vantage.
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query' # Alpha Vantage API endpoint.

# --- News Fetching Logic ---

def get_ticker_news(ticker: str, limit: int = 5) -> dict:
    """Retrieves recent news articles for a given stock ticker using the Alpha Vantage API.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'TSLA', 'AAPL').
        limit (int): The maximum number of news articles to retrieve and return. 
                     The Alpha Vantage API also has its own limits which might be different.

    Returns:
        dict: A dictionary with the following structure:
              {'status': 'success', 'news_items': list_of_news, 'message': 'Optional message'}
              {'status': 'error', 'error_message': 'Error details'}
              Each news item in `list_of_news` is a dictionary with keys like 'title', 'url', 
              'summary', 'source', 'time_published', 'overall_sentiment_label'.
    """
    if not ALPHA_VANTAGE_API_KEY:

        return {"status": "error", "error_message": "Alpha Vantage API key is not configured. Please set it in your .env file."}

    # Parameters for the Alpha Vantage API request.
    params = {
        'function': 'NEWS_SENTIMENT',       # API function to get news and sentiment.
        'tickers': ticker,                 # The stock ticker symbol.
        'apikey': ALPHA_VANTAGE_API_KEY,   # Your Alpha Vantage API key.
        'limit': str(limit),               # Number of results to return (API might have its own cap).
                                           # Alpha Vantage expects limit as string for some endpoints.
        'sort': 'LATEST'                   # Sort news by the latest first.
    }
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if "Error Message" in data:
            return {"status": "error", "error_message": f"Alpha Vantage API Error: {data['Error Message']}"}
        
        # Alpha Vantage API sometimes includes a 'Note' for high-frequency calls.
        if "Note" in data:
            # This note often indicates reaching a call limit for free tiers.
            # For a robust application, this should be handled more gracefully (e.g., logging, retries, user notification).

            # Depending on the note, you might want to return an error or a specific status.
            # If the note implies data might be missing or incomplete due to limits, it's problematic.
            # For now, we proceed if data is present, but this is a point of attention for production systems.
            pass # Continue processing if data is available despite the note.

        feed = data.get('feed', []) # 'feed' contains the list of news articles.
        if not feed:
            return {"status": "success", "news_items": [], "message": f"No news found for {ticker} via Alpha Vantage."}

        news_items = []
        # Process each news item from the feed, respecting the requested limit.
        for item in feed[:limit]: 
            news_items.append({
                "title": item.get('title', 'N/A'), # Provide default if key is missing
                "url": item.get('url'),
                "summary": item.get('summary', 'No summary available.'),
                "source": item.get('source', 'N/A'),
                "time_published": item.get('time_published'), # Format: YYYYMMDDTHHMMSS
                "overall_sentiment_label": item.get('overall_sentiment_label', 'Neutral')
            })
        return {"status": "success", "news_items": news_items}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Error fetching news from Alpha Vantage: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred while fetching news: {str(e)}"}

# Wrap the `get_ticker_news` function as a FunctionTool for the ADK agent.
 ticker_news_tool = FunctionTool(
    fn=get_ticker_news,
    name="get_ticker_news_tool",
    description="Fetches recent news articles for a specified stock ticker. Input is the ticker symbol string."
)

# --- Agent Definition ---
# Define the ADK Agent that uses the `ticker_news_tool`.

ticker_news_agent = Agent(
    name="ticker_news_sub_agent",
    model="gemini-1.5-flash", # Or another suitable model.
    description="A specialized sub-agent that retrieves the latest news articles for a given stock ticker.",
    instruction=(
        "You are a financial news assistant. Your sole task is to use the 'get_ticker_news_tool' "
        "to fetch recent news articles for the provided stock ticker symbol. "
        "Relay the results from the tool, whether it's a list of news items or an error message. "
        "Do not perform any other actions or analysis."
    ),
    tools=[
        ticker_news_tool
    ]
)