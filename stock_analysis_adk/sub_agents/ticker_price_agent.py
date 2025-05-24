# sub_agents/ticker_price_agent.py

# This file defines a specialized sub-agent for fetching the current trading price
# of a stock ticker using the Alpha Vantage API.

import os
import requests
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv # For managing API keys.

# --- Environment Variable Loading ---
# Load environment variables, particularly ALPHA_VANTAGE_API_KEY.
# Assumes the .env file is at the project root: `c:\Project\Intership_Test_AI_Agent\.env`.
project_root_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

if os.path.exists(project_root_env_path):
    load_dotenv(dotenv_path=project_root_env_path)
else:
    if not load_dotenv(): # Fallback to current working directory
        print(f"Warning: .env file not found at {project_root_env_path} or CWD. ALPHA_VANTAGE_API_KEY might be missing.")

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query' # Alpha Vantage API endpoint.

# --- Price Fetching Logic ---

def get_ticker_current_price(ticker: str) -> dict:
    """Fetches the latest trading price for a given stock ticker using Alpha Vantage's GLOBAL_QUOTE.
    Includes a fallback to daily time series if GLOBAL_QUOTE is insufficient.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'TSLA', 'AAPL').

    Returns:
        dict: A dictionary with the following structure:
              {'status': 'success', 'ticker': str, 'price': str, 'last_refreshed': str, 'note': 'Optional'}
              {'status': 'error', 'error_message': 'Error details'}
              The 'price' is returned as a string as provided by the API.
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"status": "error", "error_message": "Alpha Vantage API key is not configured. Please set it in your .env file."}

    # Parameters for the Alpha Vantage GLOBAL_QUOTE endpoint.
    params = {
        'function': 'GLOBAL_QUOTE',         # API function for the latest price.
        'symbol': ticker,                  # The stock ticker symbol.
        'apikey': ALPHA_VANTAGE_API_KEY    # Your Alpha Vantage API key.
    }
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            return {"status": "error", "error_message": f"Alpha Vantage API Error (GLOBAL_QUOTE): {data['Error Message']}"}
        
        if "Note" in data:
            # Handle API notes, often related to call frequency limits for free tiers.

            # If the note suggests data might be incomplete, it's a concern for production.
            pass # Proceed if data is present, but this needs careful handling in production.

        global_quote = data.get('Global Quote')
        
        # Check if Global Quote data is valid and contains the price.
        if global_quote and global_quote.get('05. price') and global_quote.get('05. price') != '0.0000': # also check for zero price which can be an indicator of no data
            price = global_quote.get('05. price')
            last_refreshed = global_quote.get('07. latest trading day') # Date of the latest trading day.
            # Additional useful fields: '02. open', '03. high', '04. low', '06. volume', '08. previous close', '09. change', '10. change percent'
            return {"status": "success", 
                    "ticker": ticker, 
                    "price": price, 
                    "last_refreshed": last_refreshed,
                    "open": global_quote.get('02. open'),
                    "high": global_quote.get('03. high'),
                    "low": global_quote.get('04. low'),
                    "volume": global_quote.get('06. volume'),
                    "previous_close": global_quote.get('08. previous close'),
                    "change": global_quote.get('09. change'),
                    "change_percent": global_quote.get('10. change percent')
                    }
        else:
            # Fallback to daily time series if Global Quote is empty, lacks price, or returns zero price.
            # This can happen for less common tickers, during non-trading hours, or due to API limits.

            return get_latest_daily_price(ticker)

    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Error fetching price from Alpha Vantage: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred while fetching price: {str(e)}"}

def get_latest_daily_price(ticker: str) -> dict:
    """Fallback function to get the latest closing price from Alpha Vantage's TIME_SERIES_DAILY_ADJUSTED.
    Used when GLOBAL_QUOTE does not provide a valid current price.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: Similar structure to get_ticker_current_price, with a note indicating fallback.
    """
    # Parameters for the TIME_SERIES_DAILY_ADJUSTED endpoint.
    params_daily = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED', # API function for daily historical data.
        'symbol': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'outputsize': 'compact' # 'compact' for the latest 100 data points, 'full' for more.
    }
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params_daily)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            return {"status": "error", "error_message": f"Alpha Vantage API Error (TIME_SERIES_DAILY): {data['Error Message']}"}
        if "Note" in data:

            pass # Proceed if data is present.

        time_series = data.get('Time Series (Daily)')
        if not time_series:
            return {"status": "error", "error_message": f"No daily time series data found for {ticker} in fallback."}
        
        # Get the data for the most recent day available in the time series.
        latest_date = sorted(time_series.keys(), reverse=True)[0]
        latest_day_data = time_series[latest_date]
        
        # Use the closing price from the latest day.
        price = latest_day_data.get('4. close') 
        # Could also use '5. adjusted close' if preferred.
        
        if not price:
             return {"status": "error", "error_message": f"Could not extract closing price from daily data for {ticker} on {latest_date}."}

        return {"status": "success", 
                "ticker": ticker, 
                "price": price, 
                "last_refreshed": latest_date, 
                "note": "Price is the closing price from the latest available trading day (daily series fallback).",
                "open": latest_day_data.get('1. open'),
                "high": latest_day_data.get('2. high'),
                "low": latest_day_data.get('3. low'),
                "volume": latest_day_data.get('6. volume') # Note: key is '6. volume' for daily, '06. volume' for global quote
                }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Network error in daily price fallback for {ticker}: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"Unexpected error in daily price fallback for {ticker}: {str(e)}"}

# Wrap the `get_ticker_current_price` function as a FunctionTool.
 ticker_price_tool = FunctionTool(
    fn=get_ticker_current_price,
    name="get_ticker_current_price_tool",
    description="Fetches the current or latest closing stock price for a given ticker symbol. Input is the ticker string."
)

# --- Agent Definition ---
# Define the ADK Agent that uses the `ticker_price_tool`.

ticker_price_agent = Agent(
    name="ticker_price_sub_agent",
    model="gemini-1.5-flash", # Or another suitable model.
    description="A specialized sub-agent that retrieves the current stock price for a given ticker symbol.",
    instruction=(
        "You are a financial data assistant. Your sole task is to use the 'get_ticker_current_price_tool' "
        "to fetch the latest trading price for the provided stock ticker symbol. "
        "Relay the results from the tool, including the price, last refreshed time, and any other relevant details provided. "
        "If an error occurs, report the error message from the tool. Do not perform any other actions."
    ),
    tools=[
        ticker_price_tool
    ]
)