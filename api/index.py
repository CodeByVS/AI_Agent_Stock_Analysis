import os
import re
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Agent Stock Analysis API")

# Enable CORS for local development (and standard endpoints)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel handles origins; enable all for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'

# LLM Keys
HF_API_KEY = os.getenv('HF_API_KEY') or os.getenv('HF_TOKEN')

class QueryRequest(BaseModel):
    query: str

# Mock data for fallback to prevent rate-limit crashes and show complete visual charts
MOCK_STOCK_DATA = {
    "AAPL": {"price": 182.41, "change": 1.25, "change_percent": "+0.69%", "high": 183.92, "low": 180.88, "volume": 52400000, "name": "Apple Inc."},
    "TSLA": {"price": 177.46, "change": -4.82, "change_percent": "-2.64%", "high": 184.20, "low": 176.80, "volume": 86200000, "name": "Tesla Inc."},
    "NVDA": {"price": 1150.25, "change": 24.50, "change_percent": "+2.18%", "high": 1158.10, "low": 1130.50, "volume": 42100000, "name": "NVIDIA Corporation"},
    "MSFT": {"price": 415.13, "change": -2.34, "change_percent": "-0.56%", "high": 418.40, "low": 412.20, "volume": 22400000, "name": "Microsoft Corporation"},
    "AMZN": {"price": 181.28, "change": 0.45, "change_percent": "+0.25%", "high": 183.10, "low": 179.80, "volume": 31500000, "name": "Amazon.com Inc."},
    "GOOGL": {"price": 173.50, "change": 1.12, "change_percent": "+0.65%", "high": 175.10, "low": 171.80, "volume": 25000000, "name": "Alphabet Inc."},
}

MOCK_NEWS = {
    "AAPL": [
        {"title": "Apple Intelligence unveiled at WWDC", "summary": "Apple announces its new suite of AI features integrated directly into iOS, iPadOS, and macOS.", "url": "https://apple.com", "time_published": "20260601T100000", "source": "TechCrunch"},
        {"title": "Apple suppliers ramp up production for iPhone 18", "summary": "Supply chain sources report increased orders from Apple for next-generation chips.", "url": "https://apple.com", "time_published": "20260602T083000", "source": "Bloomberg"}
    ],
    "TSLA": [
        {"title": "Tesla delivery numbers beat Q2 expectations", "summary": "Tesla reports deliveries of 443,956 vehicles, topping average consensus projections.", "url": "https://tesla.com", "time_published": "20260603T090000", "source": "Reuters"},
        {"title": "Tesla advances Full Self-Driving deployment in China", "summary": "Tesla plans to launch FSD Beta in Shanghai as regulatory clearances advance.", "url": "https://tesla.com", "time_published": "20260602T140000", "source": "CNBC"}
    ],
    "NVDA": [
        {"title": "NVIDIA hits record valuation as AI chip demand surges", "summary": "Nvidia stock closes at record high, solidifying its place as one of the world's most valuable companies.", "url": "https://nvidia.com", "time_published": "20260603T160000", "source": "MarketWatch"},
        {"title": "NVIDIA introduces new Rubin architecture at Computex", "summary": "CEO Jensen Huang reveals the successor to Blackwell, set for 2026 release.", "url": "https://nvidia.com", "time_published": "20260602T110000", "source": "The Verge"}
    ]
}

def generate_mock_historical(ticker: str, days: int = 30) -> list:
    base_price = MOCK_STOCK_DATA.get(ticker, {"price": 150.0})["price"]
    import random
    random.seed(hash(ticker)) # Consistent mock data
    
    historical = []
    current_date = datetime.now()
    
    for i in range(days):
        date_str = (current_date - timedelta(days=days - i)).strftime("%Y-%m-%d")
        # Random price walk
        change_pct = random.uniform(-0.03, 0.03)
        close_price = base_price * (1 + change_pct * (i / days))
        open_price = close_price * (1 - random.uniform(-0.015, 0.015))
        high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.01))
        low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.01))
        volume = int(random.uniform(10, 100) * 1000000)
        
        historical.append({
            "date": date_str,
            "Open": round(open_price, 2),
            "High": round(high_price, 2),
            "Low": round(low_price, 2),
            "Close": round(close_price, 2),
            "Volume": volume
        })
    return historical

# --- Helper Functions ---

def extract_ticker(query: str) -> str:
    """Helper to extract stock ticker from query string."""
    query_lower = query.lower()
    ticker_mapping = {
        'tesla': 'TSLA', 'palantir': 'PLTR', 'nvidia': 'NVDA', 'apple': 'AAPL',
        'google': 'GOOGL', 'alphabet': 'GOOGL', 'microsoft': 'MSFT', 'amazon': 'AMZN',
        'meta': 'META', 'facebook': 'META', 'netflix': 'NFLX', 'ibm': 'IBM',
        'intel': 'INTC', 'amd': 'AMD', 'salesforce': 'CRM', 'oracle': 'ORCL',
        'zoom': 'ZM', 'uber': 'UBER', 'lyft': 'LYFT', 'airbnb': 'ABNB',
        'coinbase': 'COIN', 'robinhood': 'HOOD'
    }
    
    for name, symbol in ticker_mapping.items():
        if name in query_lower:
            return symbol
            
    # Try Regex for uppercase letter words between 2 and 5 chars
    matches = re.findall(r'\b[A-Z]{2,5}\b', query)
    if matches:
        return matches[0]
        
    return "AAPL" # Default fallback if nothing found

# --- Core API Calls (with mock fallbacks on limit/errors) ---

def generate_dynamic_quote(ticker: str) -> dict:
    ticker = ticker.upper()
    if ticker in MOCK_STOCK_DATA:
        return MOCK_STOCK_DATA[ticker]
        
    seed_val = sum(ord(c) for c in ticker)
    import random
    random.seed(seed_val)
    
    price = round(random.uniform(10.0, 500.0), 2)
    change = round(random.uniform(-15.0, 15.0), 2)
    change_pct = round((change / (price - change)) * 100, 2) if (price - change) else 0.0
    change_pct_str = f"{'+' if change >= 0 else ''}{change_pct}%"
    high = round(price + random.uniform(0.1, 5.0), 2)
    low = round(price - random.uniform(0.1, 5.0), 2)
    volume = int(random.uniform(1.0, 80.0) * 1000000)
    
    return {
        "price": price,
        "change": change,
        "change_percent": change_pct_str,
        "high": high,
        "low": low,
        "volume": volume,
        "name": f"{ticker} Corporation"
    }

def generate_dynamic_news_with_hf(ticker: str) -> list:
    ticker = ticker.upper()
    if ticker in MOCK_NEWS:
        return MOCK_NEWS[ticker]
        
    if HF_API_KEY:
        prompt = f"""
        Generate a JSON array containing 2 realistic financial news articles for the stock ticker: {ticker}.
        Each article must be a JSON object with:
        - "title": A short realistic headline
        - "summary": A 1-2 sentence description of the news
        - "source": A financial media name (e.g. Reuters, Bloomberg, CNBC)
        
        Only return the raw JSON array. No explanations, no markdown formatting, no code block backticks.
        """
        try:
            raw_response = query_huggingface(prompt)
            cleaned = raw_response.replace("```json", "").replace("```", "").strip()
            start = cleaned.find('[')
            end = cleaned.rfind(']')
            if start != -1 and end != -1:
                json_str = cleaned[start:end+1]
                articles = json.loads(json_str)
                if isinstance(articles, list) and len(articles) > 0:
                    output_news = []
                    for i, art in enumerate(articles[:2]):
                        output_news.append({
                            "title": art.get("title", f"{ticker} Market Activity Update"),
                            "summary": art.get("summary", f"Trading activity indicates consolidation for {ticker} share price."),
                            "url": f"https://finance.yahoo.com/quote/{ticker}",
                            "time_published": (datetime.now() - timedelta(hours=i*6 + 1)).strftime("%Y%m%dT%H%M%S"),
                            "source": art.get("source", "Bloomberg")
                        })
                    return output_news
        except Exception:
            pass
            
    # Heuristic template fallback
    seed_val = sum(ord(c) for c in ticker)
    import random
    random.seed(seed_val)
    
    headlines_templates = [
        ("{ticker} expands AI capabilities in latest product update", "{ticker} announced new features integrating advanced neural network workflows into its enterprise dashboards.", "TechCrunch"),
        ("{ticker} quarterly earnings outperform Wall Street projections", "{ticker} reported earnings per share that exceeded analyst forecasts, driven by strong growth in its cloud division.", "Bloomberg"),
        ("Investors pivot to {ticker} amid sector consolidation", "Shares of {ticker} experienced increased trading volumes as institutional portfolios reallocated assets.", "Reuters"),
        ("Supply chain efficiencies boost {ticker} operating margins", "{ticker} management noted that optimization in procurement helped offset inflationary pressures.", "CNBC")
    ]
    
    chosen = random.sample(headlines_templates, min(len(headlines_templates), 2))
    news_items = []
    for i, (title_tmpl, desc_tmpl, source) in enumerate(chosen):
        title = title_tmpl.format(ticker=ticker)
        summary = desc_tmpl.format(ticker=ticker)
        news_items.append({
            "title": title,
            "summary": summary,
            "url": f"https://finance.yahoo.com/quote/{ticker}",
            "time_published": (datetime.now() - timedelta(hours=i*6 + 2)).strftime("%Y%m%dT%H%M%S"),
            "source": source
        })
    return news_items

def fetch_price_data(ticker: str) -> dict:
    if not ALPHA_VANTAGE_API_KEY:
        mock = generate_dynamic_quote(ticker)
        return {"status": "success", "source": "mock", **mock}
        
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    try:
        res = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        res.raise_for_status()
        data = res.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            return {
                "status": "success",
                "source": "alphavantage",
                "price": float(quote.get('05. price', 0)),
                "change": float(quote.get('09. change', 0)),
                "change_percent": quote.get('10. change percent', '0%'),
                "high": float(quote.get('03. high', 0)),
                "low": float(quote.get('04. low', 0)),
                "volume": int(quote.get('06. volume', 0)),
                "name": f"{ticker} Inc."
            }
        else:
            mock = generate_dynamic_quote(ticker)
            return {"status": "success", "source": "mock (api rate limit)", **mock}
    except Exception:
        mock = generate_dynamic_quote(ticker)
        return {"status": "success", "source": "mock (exception)", **mock}

def fetch_news_data(ticker: str) -> dict:
    if not ALPHA_VANTAGE_API_KEY:
        return {"status": "success", "source": "mock", "news_items": generate_dynamic_news_with_hf(ticker)}
        
    params = {
        'function': 'NEWS_SENTIMENT',
        'tickers': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'limit': 5,
        'sort': 'LATEST'
    }
    try:
        res = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        res.raise_for_status()
        data = res.json()
        
        feed = data.get('feed', [])
        if feed:
            news_items = []
            for item in feed[:5]:
                news_items.append({
                    'title': item.get('title', 'No Title'),
                    'summary': item.get('summary', 'No Summary'),
                    'url': item.get('url', ''),
                    'time_published': item.get('time_published', ''),
                    'source': item.get('source', 'Unknown')
                })
            return {"status": "success", "source": "alphavantage", "news_items": news_items}
        else:
            return {"status": "success", "source": "mock (api rate limit)", "news_items": generate_dynamic_news_with_hf(ticker)}
    except Exception:
        return {"status": "success", "source": "mock (exception)", "news_items": generate_dynamic_news_with_hf(ticker)}

def fetch_price_change(ticker: str, timeframe: str = "7 days") -> dict:
    # Estimate based on current price
    price_info = fetch_price_data(ticker)
    price = price_info.get("price", 100.0)
    
    days_back = 7
    if "month" in timeframe.lower() or "30 days" in timeframe.lower():
        days_back = 30
    elif "today" in timeframe.lower() or "1 day" in timeframe.lower():
        days_back = 1
        
    # Generate past price by reversing current change slightly
    change = price_info.get("change", 0.0)
    past_price = price - (change * days_back * 0.4) # estimate
    change_val = price - past_price
    change_pct = (change_val / past_price) * 100 if past_price else 0
    
    return {
        "status": "success",
        "ticker": ticker,
        "timeframe": timeframe,
        "current_price": price,
        "past_price": round(past_price, 2),
        "change": round(change_val, 2),
        "change_percent": round(change_pct, 2)
    }

# --- LLM API Synthesis Routing ---

def query_huggingface(prompt: str) -> str:
    """Invokes Hugging Face Inference API for text generation."""
    # Standard instruction model
    model_id = "tiiuae/falcon-7b-instruct"
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.7, "return_full_text": False}
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "").strip()
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
        return f"Hugging Face response parsed error: {str(data)}"
    except Exception as e:
        return f"Failed HF generation: {str(e)}"


def run_heuristic_synthesis(ticker: str, price_info: dict, news_info: dict, change_info: dict) -> str:
    """Rule-based text synthesizer fallback."""
    direction = "increased" if change_info['change'] > 0 else "decreased" if change_info['change'] < 0 else "remained stable"
    analysis = f"### Stock Analysis for {ticker} (Programmatic Fallback Mode)\n\n"
    analysis += f"**Price Movement**: The stock of **{ticker}** has {direction} by **${abs(change_info['change']):.2f}** ({abs(change_info['change_percent']):.2f}%) over the {change_info['timeframe']}. The current price sits at **${price_info.get('price', 0.0):.2f}**.\n\n"
    
    news_items = news_info.get("news_items", [])
    if news_items:
        analysis += "**Recent News Insights**:\n"
        for i, news in enumerate(news_items[:3], 1):
            analysis += f"{i}. **{news['title']}** (Source: {news['source']})\n   _{news['summary'][:180]}..._\n"
        analysis += "\n"
    
    if change_info['change'] > 0:
        analysis += "**Market Factors**: The upward price momentum suggests strong buying volume. This could correlate with the positive sentiment highlighted in recent news stories, or a broader sector-wide rally.\n"
    elif change_info['change'] < 0:
        analysis += "**Market Factors**: The downward trend indicates recent sell-offs. Recent headlines should be examined to see if macroeconomic pressures, supply constraints, or weak earnings reports influenced this decline.\n"
    else:
        analysis += "**Market Factors**: Stable price activity represents standard consolidating behavior with low volatility and no sudden news catalysts.\n"
        
    return analysis

# --- API Endpoints ---

@app.get("/api/config")
def get_config():
    return {
        "alpha_vantage_configured": ALPHA_VANTAGE_API_KEY is not None,
        "hugging_face_configured": HF_API_KEY is not None,
        "active_llm": "Hugging Face" if HF_API_KEY else "Rule-based Fallback"
    }

@app.post("/api/query")
def run_query(payload: QueryRequest):
    query = payload.query
    ticker = extract_ticker(query)
    
    # 1. Fetch current price
    price_data = fetch_price_data(ticker)
    
    # 2. Fetch news
    news_data = fetch_news_data(ticker)
    
    # 3. Calculate price change
    timeframe = "7 days"
    if "today" in query.lower():
        timeframe = "today"
    elif "month" in query.lower() or "30 days" in query.lower():
        timeframe = "1 month"
    change_data = fetch_price_change(ticker, timeframe)
    
    # 4. Generate Analysis Prompt
    prompt = f"""
    You are a professional financial analysis agent. Analyze the following details for the stock ticker: {ticker}.
    
    PRICE DATA:
    Current Price: ${price_data.get('price', 0.0)}
    Change (today): {price_data.get('change_percent', '0%')}
    High/Low: ${price_data.get('high', 0.0)} / ${price_data.get('low', 0.0)}
    Volume: {price_data.get('volume', 0)}
    
    PRICE CHANGE ANALYSIS:
    Period: {change_data.get('timeframe')}
    Past Price: ${change_data.get('past_price')}
    Net Change: ${change_data.get('change')}
    Percentage Change: {change_data.get('change_percent')}%
    
    RECENT NEWS ITEMS:
    {json.dumps(news_data.get('news_items', []), indent=2)}
    
    Based on the above news articles and stock details, write a concise and professional summary explaining potential factors behind the price movements. Correlate news articles with the price change where appropriate. Make sure to present your findings clearly with markdown.
    """
    
    analysis_text = ""
    llm_source = "Rule-based Fallback"
    
    if HF_API_KEY:
        analysis_text = query_huggingface(prompt)
        llm_source = "Hugging Face"
        
    # If LLM execution failed or returned errors, fallback to rule-based synthesis
    if not analysis_text or "Failed" in analysis_text:
        analysis_text = run_heuristic_synthesis(ticker, price_data, news_data, change_data)
        llm_source = "Heuristic-based Fallback"
        
    return {
        "ticker": ticker,
        "price_data": price_data,
        "news_data": news_data,
        "change_data": change_data,
        "analysis": analysis_text,
        "llm_used": llm_source
    }

@app.get("/api/stock/{ticker}/price")
def get_price(ticker: str):
    return fetch_price_data(ticker.upper())

@app.get("/api/stock/{ticker}/news")
def get_news(ticker: str):
    return fetch_news_data(ticker.upper())

@app.get("/api/stock/{ticker}/price-change")
def get_change(ticker: str, timeframe: str = "7 days"):
    return fetch_price_change(ticker.upper(), timeframe)

@app.get("/api/stock/{ticker}/historical")
def get_historical(ticker: str):
    ticker = ticker.upper()
    if not ALPHA_VANTAGE_API_KEY:
        return generate_mock_historical(ticker)
        
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': ticker,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'outputsize': 'compact'
    }
    try:
        res = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        res.raise_for_status()
        data = res.json()
        
        time_series = data.get('Time Series (Daily)', {})
        if time_series:
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df = df.astype(float)
            df.index = pd.to_datetime(df.index)
            df.sort_index(inplace=True)
            df = df[['1. open', '2. high', '3. low', '4. close', '5. adjusted close', '6. volume']]
            df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume']
            
            # Format into clean array of dicts for Recharts
            output = []
            for date_idx, row in df.iterrows():
                output.append({
                    "date": date_idx.strftime("%Y-%m-%d"),
                    "Open": round(row["Open"], 2),
                    "High": round(row["High"], 2),
                    "Low": round(row["Low"], 2),
                    "Close": round(row["Close"], 2),
                    "Volume": int(row["Volume"])
                })
            return output
        else:
            return generate_mock_historical(ticker)
    except Exception:
        return generate_mock_historical(ticker)
