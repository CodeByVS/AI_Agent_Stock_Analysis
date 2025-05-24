# sub_agents/ticker_price_change_agent.py

# This file defines a specialized sub-agent for calculating stock price changes
# over various timeframes using Alpha Vantage API data.

import os
import requests
import datetime
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv # For managing API keys.
import pandas as pd # For efficient data handling, especially with time series.

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

# --- Price Change Calculation Logic ---

def get_ticker_price_change(ticker: str, timeframe: str = "today") -> dict:
    """Calculates the stock's price change for a given ticker and timeframe using daily adjusted data.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'TSLA', 'AAPL').
        timeframe (str): The period over which to calculate the price change.
                         Supported values (case-insensitive):
                         - 'today' or '1 day': Change from previous close to latest close.
                         - '7 days' or 'last week': Change over the last 7 calendar days (approx).
                         - '30 days', '1 month', or 'last month': Change over the last 30 calendar days (approx).
                         Defaults to 'today'.

    Returns:
        dict: A dictionary with the following structure on success:
              {
                  'status': 'success',
                  'ticker': str,
                  'timeframe_description': str, (e.g., 'since YYYY-MM-DD close' or 'from YYYY-MM-DD to YYYY-MM-DD')
                  'start_date': str (YYYY-MM-DD),
                  'start_price': float,
                  'end_date': str (YYYY-MM-DD),
                  'end_price': float,
                  'price_change': float,
                  'percentage_change': float
              }
              Or on failure:
              {'status': 'error', 'error_message': 'Error details'}
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"status": "error", "error_message": "Alpha Vantage API key is not configured. Please set it in your .env file."}

    output_size = 'compact' 

    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED', 
        'symbol': ticker,                        
        'apikey': ALPHA_VANTAGE_API_KEY,          
        'outputsize': output_size                
    }

    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            return {"status": "error", "error_message": f"Alpha Vantage API Error (TIME_SERIES_DAILY): {data['Error Message']}"}
        if "Note" in data:
            pass

        time_series_key = 'Time Series (Daily)'
        if time_series_key not in data or not data[time_series_key]:
            return {"status": "error", "error_message": f"No time series data found for {ticker}. Check ticker symbol or API response."}

        df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
        df.index = pd.to_datetime(df.index) 
        df.sort_index(ascending=False, inplace=True) 
        df['4. close'] = pd.to_numeric(df['4. close'], errors='coerce')
        df.dropna(subset=['4. close'], inplace=True) 

        if df.empty:
            return {"status": "error", "error_message": f"Time series data for {ticker} is empty or invalid after processing."}

        end_price_data = df.iloc[0]
        end_price = end_price_data['4. close']
        end_date = end_price_data.name.date() 

        start_price = None
        start_date = None
        period_description = ""
        tf_lower = timeframe.lower()

        if tf_lower in ["today", "1 day"]:
            if len(df) < 2:
                return {"status": "error", "error_message": f"Not enough historical data for {ticker} to calculate 'today's' or '1 day' change (need at least 2 data points)."}
            start_price_data = df.iloc[1] 
            start_price = start_price_data['4. close']
            start_date = start_price_data.name.date()
            period_description = f"change from {start_date.isoformat()} close to {end_date.isoformat()} close"
        
        elif tf_lower in ["7 days", "last week", "30 days", "1 month", "last month"]:
            days_offset = 7 if tf_lower in ["7 days", "last week"] else 30
            start_date_target = end_date - datetime.timedelta(days=days_offset)
            past_data_points = df[df.index.date <= start_date_target]
            
            if not past_data_points.empty:
                start_price_data = past_data_points.iloc[0] 
            elif not df.empty:
                start_price_data = df.iloc[-1] 
            else:
                return {"status": "error", "error_message": f"Insufficient historical data for {ticker} for timeframe '{timeframe}'."}

            start_price = start_price_data['4. close']
            start_date = start_price_data.name.date()
            period_description = f"change from {start_date.isoformat()} to {end_date.isoformat()} (approx. {days_offset} days)"
        else:
            return {"status": "error", "error_message": f"Unsupported timeframe: '{timeframe}'. Supported: 'today', '1 day', '7 days', 'last week', '1 month', 'last month'."}

        if start_price is None or pd.isna(start_price) or end_price is None or pd.isna(end_price):
            return {"status": "error", "error_message": f"Could not determine valid start or end price for {ticker} for timeframe '{timeframe}'. Start: {start_price}, End: {end_price}"}

        price_change = end_price - start_price
        percentage_change = (price_change / start_price) * 100 if start_price != 0 else 0


        return {
            "status": "success",
            "ticker": ticker,
            "timeframe_description": period_description,
            "start_date": start_date.isoformat(),
            "start_price": float(start_price),
            "end_date": end_date.isoformat(),
            "end_price": float(end_price),
            "price_change": float(price_change),
            "percentage_change": float(percentage_change)
        }

    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Network error fetching price change data from Alpha Vantage for {ticker}: {str(e)}"}
    except KeyError as e:
        return {"status": "error", "error_message": f"Data format error from Alpha Vantage for {ticker} (missing key: {str(e)})."}
    except ValueError as e:
        return {"status": "error", "error_message": f"Data conversion error for {ticker}: {str(e)}"}
    except IndexError as e:
        return {"status": "error", "error_message": f"Not enough data points for {ticker} to calculate change for timeframe '{timeframe}': {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred while calculating price change for {ticker}: {str(e)}"}


ticker_price_change_tool = FunctionTool(
    fn=get_ticker_price_change,
    name="get_ticker_price_change_tool",
    description="Calculates the stock price change (absolute and percentage) for a given ticker over a specified timeframe (e.g., 'today', '7 days', '1 month'). Input is a dict with 'ticker' and 'timeframe'."
)


ticker_price_change_agent = Agent(
    name="ticker_price_change_sub_agent",
    model="gemini-1.5-flash", 
    description="A specialized sub-agent that calculates stock price changes (value and percentage) for a given ticker over a specified timeframe.",
    instruction=(
        "You are a financial data assistant. Your sole task is to use the 'get_ticker_price_change_tool' "
        "to calculate the price change for the provided stock ticker and timeframe. "
        "The input to the tool should be a dictionary with 'ticker' (string) and 'timeframe' (string, e.g., 'today', '7 days', '1 month'). "
        "Relay the full results from the tool, including all details like start/end prices, dates, and changes. "
        "If an error occurs, report the error message from the tool. Do not perform any other actions."
    ),
    tools=[
        ticker_price_change_tool
    ]
)