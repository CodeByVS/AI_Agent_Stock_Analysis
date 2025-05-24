import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

# Load environment variables from .env file for API key management
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'

# --- Core Agent-like Functions ---
# These functions mimic the capabilities of the individual agents
# in the original Google ADK multi-agent system.

def extract_ticker_from_query(query: str) -> dict:
    """Identifies a stock ticker from a natural language query.
    Uses a predefined mapping and regex for ticker extraction.
    
    Args:
        query (str): The user's input query.
        
    Returns:
        dict: A dictionary containing the status and identified ticker or an error message.
    """
    query_lower = query.lower()
    
    # Extended ticker mapping
    ticker_mapping = {
        'tesla': 'TSLA',
        'palantir': 'PLTR', 
        'nvidia': 'NVDA',
        'apple': 'AAPL',
        'google': 'GOOGL',
        'alphabet': 'GOOGL',
        'microsoft': 'MSFT',
        'amazon': 'AMZN',
        'meta': 'META',
        'facebook': 'META',
        'netflix': 'NFLX',
        'ibm': 'IBM',
        'intel': 'INTC',
        'amd': 'AMD',
        'salesforce': 'CRM',
        'oracle': 'ORCL',
        'zoom': 'ZM',
        'uber': 'UBER',
        'lyft': 'LYFT',
        'airbnb': 'ABNB',
        'coinbase': 'COIN',
        'robinhood': 'HOOD'
    }
    
    for company, ticker in ticker_mapping.items():
        if company in query_lower:
            return {"status": "success", "ticker": ticker}
    
    # Try to extract ticker symbols directly (3-4 uppercase letters)
    import re
    ticker_pattern = r'\b[A-Z]{2,5}\b'
    matches = re.findall(ticker_pattern, query.upper())
    if matches:
        return {"status": "success", "ticker": matches[0]}
    
    return {"status": "error", "error_message": f"Could not identify a stock ticker in: '{query}'"}

def get_ticker_news(ticker: str, limit: int = 5) -> dict:
    """Fetches recent news articles for a given stock ticker using Alpha Vantage API.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        limit (int): The maximum number of news items to return.
        
    Returns:
        dict: A dictionary with news items or an error message.
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"status": "error", "error_message": "Alpha Vantage API key not configured."}
    
    params = {
        'function': 'NEWS_SENTIMENT',
        'tickers': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'limit': limit,
        'sort': 'LATEST'
    }
    
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            return {"status": "error", "error_message": f"API Error: {data['Error Message']}"}
        
        feed = data.get('feed', [])
        if not feed:
            return {"status": "success", "news_items": [], "message": f"No news found for {ticker}."}
        
        news_items = []
        for item in feed[:limit]:
            news_items.append({
                'title': item.get('title', 'No title'),
                'summary': item.get('summary', 'No summary'),
                'url': item.get('url', ''),
                'time_published': item.get('time_published', ''),
                'source': item.get('source', 'Unknown')
            })
        
        return {"status": "success", "news_items": news_items}
    
    except Exception as e:
        return {"status": "error", "error_message": f"Error fetching news: {str(e)}"}

def get_ticker_current_price(ticker: str) -> dict:
    """Retrieves the latest trading price for a given stock ticker from Alpha Vantage.
    
    Args:
        ticker (str): The stock ticker symbol.
        
    Returns:
        dict: A dictionary with current price information or an error message.
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"status": "error", "error_message": "Alpha Vantage API key not configured."}
    
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            return {"status": "error", "error_message": f"API Error: {data['Error Message']}"}
        
        quote = data.get('Global Quote', {})
        if not quote:
            return {"status": "error", "error_message": f"No price data found for {ticker}."}
        
        return {
            "status": "success",
            "ticker": ticker,
            "price": float(quote.get('05. price', 0)),
            "change": float(quote.get('09. change', 0)),
            "change_percent": quote.get('10. change percent', '0%'),
            "last_updated": quote.get('07. latest trading day', '')
        }
    
    except Exception as e:
        return {"status": "error", "error_message": f"Error fetching price: {str(e)}"}

def get_ticker_price_change(ticker: str, timeframe: str = "7 days") -> dict:
    """Calculates the price change of a stock over a specified timeframe.
    
    Args:
        ticker (str): The stock ticker symbol.
        timeframe (str): The period for price change calculation (e.g., "7 days", "1 month").
        
    Returns:
        dict: A dictionary with price change details or an error message.
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"status": "error", "error_message": "Alpha Vantage API key not configured."}
    
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'outputsize': 'compact'
    }
    
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            return {"status": "error", "error_message": f"API Error: {data['Error Message']}"}
        
        time_series = data.get('Time Series (Daily)', {})
        if not time_series:
            return {"status": "error", "error_message": f"No historical data found for {ticker}."}
        
        dates = sorted(time_series.keys(), reverse=True)
        if len(dates) < 2:
            return {"status": "error", "error_message": "Insufficient data for comparison."}
        
        # Parse timeframe
        days_back = 1
        if "7 days" in timeframe.lower() or "week" in timeframe.lower():
            days_back = 7
        elif "month" in timeframe.lower() or "30 days" in timeframe.lower():
            days_back = 30
        elif "today" in timeframe.lower():
            days_back = 1
        
        current_price = float(time_series[dates[0]]['4. close'])
        
        # Find price from days_back ago
        past_price = current_price
        if len(dates) > days_back:
            past_price = float(time_series[dates[min(days_back, len(dates)-1)]]['4. close'])
        
        change = current_price - past_price
        change_percent = (change / past_price) * 100 if past_price != 0 else 0
        
        return {
            "status": "success",
            "ticker": ticker,
            "timeframe": timeframe,
            "current_price": current_price,
            "past_price": past_price,
            "change": change,
            "change_percent": change_percent,
            "current_date": dates[0],
            "past_date": dates[min(days_back, len(dates)-1)] if len(dates) > days_back else dates[-1]
        }
    
    except Exception as e:
        return {"status": "error", "error_message": f"Error calculating price change: {str(e)}"}

def fetch_stock_data(symbol: str) -> pd.DataFrame | None:
    """Fetches historical daily stock data for visualization purposes from Alpha Vantage.
    
    Args:
        symbol (str): The stock ticker symbol.
        
    Returns:
        pd.DataFrame | None: A Pandas DataFrame with historical stock data, or None on error.
    """
    if not ALPHA_VANTAGE_API_KEY:
        return None
    
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'outputsize': 'compact'
    }
    
    try:
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            st.error(f"Alpha Vantage API Error: {data['Error Message']}")
            return None
        
        time_series_key = 'Time Series (Daily)'
        if time_series_key in data:
            df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
            df = df.astype(float)
            df.index = pd.to_datetime(df.index)
            df.sort_index(inplace=True)
            df = df[['1. open', '2. high', '3. low', '4. close', '5. adjusted close', '6. volume']]
            df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume']
            return df
        else:
            st.error(f"No time series data found for {symbol}")
            return None
    
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def analyze_stock_movement(ticker: str, news_data: dict, price_change_data: dict) -> str:
    """Generates a textual analysis of stock movement based on news and price change data.
    This function acts as the 'ticker_analysis_agent'.
    
    Args:
        ticker (str): The stock ticker symbol.
        news_data (dict): Data from get_ticker_news.
        price_change_data (dict): Data from get_ticker_price_change.
        
    Returns:
        str: A markdown-formatted string with the stock movement analysis.
    """
    analysis = f"## Stock Analysis for {ticker}\n\n"
    
    # Price analysis
    if price_change_data.get('status') == 'success':
        change = price_change_data['change']
        change_percent = price_change_data['change_percent']
        timeframe = price_change_data['timeframe']
        
        direction = "increased" if change > 0 else "decreased" if change < 0 else "remained stable"
        analysis += f"**Price Movement**: The stock has {direction} by ${abs(change):.2f} ({abs(change_percent):.2f}%) over the {timeframe}.\n\n"
    
    # News analysis
    if news_data.get('status') == 'success' and news_data.get('news_items'):
        analysis += "**Recent News Impact**:\n"
        for i, news in enumerate(news_data['news_items'][:3], 1):
            analysis += f"{i}. **{news['title']}** - {news['summary'][:200]}...\n"
        analysis += "\n"
    
    # Correlation analysis
    if price_change_data.get('status') == 'success':
        if price_change_data['change'] > 0:
            analysis += "**Potential Factors**: The positive price movement may be attributed to favorable market sentiment, positive news coverage, or broader market trends.\n"
        elif price_change_data['change'] < 0:
            analysis += "**Potential Factors**: The negative price movement could be due to market concerns, negative news, or broader market downturns.\n"
        else:
            analysis += "**Potential Factors**: The stable price suggests balanced market sentiment with no significant catalysts.\n"
    
    return analysis

# --- Streamlit User Interface ---

# Page Configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Multi-Agent Stock Analysis System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main Title
st.title("🤖 Multi-Agent Stock Analysis System")
st.markdown("An intelligent system for stock insights, powered by a multi-agent architecture.")

# Sidebar Navigation
st.sidebar.header("📊 Analysis Modes")
mode = st.sidebar.radio(
    "Choose an analysis mode:",
    ("Natural Language Query", "Stock Data Visualization", "Manual Agent Analysis"),
    captions=["Ask questions in plain English.", "Explore charts and data.", "Test individual agent functions."]
)

# --- Mode: Natural Language Query ---
if mode == "Natural Language Query":
    st.header("💬 Natural Language Stock Query")
    st.markdown("Ask questions about stocks like: *'Why did Tesla stock drop today?'* or *'What's the news on NVDA?'*")
    
    query = st.text_input("Enter your stock question:", placeholder="e.g., Tell me about Apple stock")
    
    if query and st.button("Analyze", type="primary"):
        with st.spinner("Processing your query..."):
            # Step 1: Extract ticker
            ticker_result = extract_ticker_from_query(query)
            
            if ticker_result['status'] == 'error':
                st.error(f"❌ {ticker_result['error_message']}")
            else:
                ticker = ticker_result['ticker']
                st.success(f"✅ Identified ticker: **{ticker}**")
                
                # Create columns for parallel processing
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"📰 Recent News for {ticker}")
                    news_result = get_ticker_news(ticker)
                    
                    if news_result['status'] == 'success':
                        if news_result['news_items']:
                            for news in news_result['news_items']:
                                with st.expander(f"📄 {news['title']}"):
                                    st.write(f"**Source:** {news['source']}")
                                    st.write(f"**Published:** {news['time_published']}")
                                    st.write(f"**Summary:** {news['summary']}")
                                    if news['url']:
                                        st.markdown(f"[Read full article]({news['url']})")
                        else:
                            st.info("No recent news found.")
                    else:
                        st.error(f"Error fetching news: {news_result['error_message']}")
                
                with col2:
                    st.subheader(f"💰 Price Information for {ticker}")
                    
                    # Current price
                    price_result = get_ticker_current_price(ticker)
                    if price_result['status'] == 'success':
                        st.metric(
                            label="Current Price",
                            value=f"${price_result['price']:.2f}",
                            delta=f"{price_result['change']:.2f} ({price_result['change_percent']})"
                        )
                        st.caption(f"Last updated: {price_result['last_updated']}")
                    else:
                        st.error(f"Error fetching price: {price_result['error_message']}")
                    
                    # Price change analysis
                    timeframe = "7 days"
                    if "today" in query.lower():
                        timeframe = "today"
                    elif "week" in query.lower() or "7 days" in query.lower():
                        timeframe = "7 days"
                    elif "month" in query.lower():
                        timeframe = "1 month"
                    
                    change_result = get_ticker_price_change(ticker, timeframe)
                    if change_result['status'] == 'success':
                        st.metric(
                            label=f"Change ({timeframe})",
                            value=f"${change_result['change']:.2f}",
                            delta=f"{change_result['change_percent']:.2f}%"
                        )
                    else:
                        st.error(f"Error calculating price change: {change_result['error_message']}")
                
                # Comprehensive analysis
                st.subheader("🔍 AI Analysis")
                if ticker_result['status'] == 'success':
                    analysis = analyze_stock_movement(ticker, news_result, change_result)
                    st.markdown(analysis)

# --- Mode: Stock Data Visualization ---
elif mode == "Stock Data Visualization":
    st.header("📊 Interactive Stock Data Visualization")
    
    stock_symbol = st.text_input("Enter Stock Symbol:", value="AAPL").upper()
    
    if stock_symbol:
        with st.spinner(f"Loading data for {stock_symbol}..."):
            stock_df = fetch_stock_data(stock_symbol)
        
        if stock_df is not None and not stock_df.empty:
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            latest_price = stock_df['Close'].iloc[-1]
            prev_price = stock_df['Close'].iloc[-2] if len(stock_df) > 1 else latest_price
            price_change = latest_price - prev_price
            price_change_pct = (price_change / prev_price) * 100 if prev_price != 0 else 0
            
            with col1:
                st.metric("Latest Price", f"${latest_price:.2f}", f"{price_change:.2f} ({price_change_pct:.2f}%)")
            with col2:
                st.metric("Volume", f"{stock_df['Volume'].iloc[-1]:,.0f}")
            with col3:
                st.metric("52W High", f"${stock_df['High'].max():.2f}")
            with col4:
                st.metric("52W Low", f"${stock_df['Low'].min():.2f}")
            
            # Chart selection
            chart_type = st.selectbox("Select Chart Type", ["Candlestick", "Line Chart", "OHLC"])
            
            if chart_type == "Candlestick":
                fig = go.Figure(data=[go.Candlestick(
                    x=stock_df.index,
                    open=stock_df['Open'],
                    high=stock_df['High'],
                    low=stock_df['Low'],
                    close=stock_df['Close'],
                    name=stock_symbol
                )])
                fig.update_layout(title=f"{stock_symbol} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Line Chart":
                fig = px.line(stock_df, x=stock_df.index, y='Close', title=f"{stock_symbol} Price Chart")
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "OHLC":
                fig = go.Figure(data=[go.Ohlc(
                    x=stock_df.index,
                    open=stock_df['Open'],
                    high=stock_df['High'],
                    low=stock_df['Low'],
                    close=stock_df['Close'],
                    name=stock_symbol
                )])
                fig.update_layout(title=f"{stock_symbol} OHLC Chart", xaxis_title="Date", yaxis_title="Price")
                st.plotly_chart(fig, use_container_width=True)
            
            # Volume chart
            st.subheader("Trading Volume")
            fig_volume = px.bar(stock_df, x=stock_df.index, y='Volume', title=f"{stock_symbol} Trading Volume")
            st.plotly_chart(fig_volume, use_container_width=True)
            
            # Data table
            st.subheader("Recent Data")
            st.dataframe(stock_df.tail(10))

# --- Mode: Manual Agent Analysis ---
elif mode == "Manual Agent Analysis":
    st.header("🔧 Manual Agent Testing")
    st.markdown("Test the core data retrieval and analysis functions individually.")
    
    ticker_input = st.text_input("Enter Stock Ticker:", value="TSLA").upper()
    
    if ticker_input:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Get Current Price", use_container_width=True):
                with st.spinner("Fetching price data..."):
                    result = get_ticker_current_price(ticker_input)
                    if result['status'] == 'success':
                        st.success("Price data retrieved successfully!")
                        st.json(result)
                    else:
                        st.error(f"Error: {result['error_message']}")
            
            if st.button("📰 Get Recent News", use_container_width=True):
                with st.spinner("Fetching news data..."):
                    result = get_ticker_news(ticker_input)
                    if result['status'] == 'success':
                        st.success("News data retrieved successfully!")
                        for news in result['news_items']:
                            st.write(f"**{news['title']}**")
                            st.write(news['summary'])
                            st.write("---")
                    else:
                        st.error(f"Error: {result['error_message']}")
        
        with col2:
            timeframe = st.selectbox("Select Timeframe", ["today", "7 days", "1 month"])
            
            if st.button("📈 Calculate Price Change", use_container_width=True):
                with st.spinner("Calculating price change..."):
                    result = get_ticker_price_change(ticker_input, timeframe)
                    if result['status'] == 'success':
                        st.success("Price change calculated successfully!")
                        st.json(result)
                    else:
                        st.error(f"Error: {result['error_message']}")
            
            if st.button("🤖 Generate Analysis", use_container_width=True):
                with st.spinner("Generating comprehensive analysis..."):
                    news_data = get_ticker_news(ticker_input)
                    price_data = get_ticker_price_change(ticker_input, timeframe)
                    analysis = analyze_stock_movement(ticker_input, news_data, price_data)
                    st.markdown(analysis)

# --- Footer and API Key Status ---
st.sidebar.markdown("---")
if not ALPHA_VANTAGE_API_KEY:
    st.sidebar.error("⚠️ API Key Not Found! Please set `ALPHA_VANTAGE_API_KEY` in your `.env` file.")
else:
    st.sidebar.success("✅ Alpha Vantage API Key Loaded")

st.markdown("---")
st.caption("Multi-Agent Stock Analysis System - v1.0 | Developed with Streamlit and Python")