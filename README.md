# Multi-Agent Stock Analysis System

🤖 **A Comprehensive Stock Analysis Platform with Multi-Agent Architecture and Streamlit Interface**

## 🚀 Quick Start

**To run the application:**

1.  **Ensure Prerequisites:**
    *   Python 3.8+ installed.
    *   You have an Alpha Vantage API key (get one free from [alphavantage.co](https://www.alphavantage.co/support/#api-key)).

2.  **Set up Environment Variable:**
    *   In the project root (`c:\Project\Intership_Test_AI_Agent`), create a file named `.env`.
    *   Add your Alpha Vantage API key to it:
        ```env
        ALPHA_VANTAGE_API_KEY="YOUR_ACTUAL_API_KEY"
        ```
        (Replace `YOUR_ACTUAL_API_KEY` with your key).

3.  **Run the Setup Script (Recommended for first time):**
    This script checks Python version, installs dependencies, and launches the app.
    ```bash
    cd c:\Project\Intership_Test_AI_Agent
    python setup_and_run.py
    ```

4.  **Manual Launch (if dependencies are already installed):**
    ```bash
    cd c:\Project\Intership_Test_AI_Agent
    # Ensure dependencies are installed: pip install -r requirements.txt
    streamlit run unified_stock_analysis_app.py
    ```

## Overview

This project demonstrates a complete multi-agent stock analysis system with two primary components:

1.  **🎯 Unified Streamlit Application (`unified_stock_analysis_app.py`)**: This is the primary, user-facing application. It provides an interactive interface for stock analysis using natural language queries, data visualization, and manual agent interaction. It directly implements the logic for fetching and processing stock data and news using the Alpha Vantage API.
2.  **🤖 Google ADK Multi-Agent System (`stock_analysis_adk/`)**: This self-contained directory serves as a **reference implementation** of a multi-agent system built with the Google Agent Development Kit (ADK). It demonstrates how the same stock analysis tasks can be broken down and orchestrated among specialized agents (e.g., ticker identification, news fetching, price analysis). This part is for understanding ADK concepts and is not directly run by the main Streamlit application but shares conceptual logic.

The system processes natural language queries, fetches real-time stock data, analyzes news sentiment, and generates comprehensive investment insights through specialized AI agents.

## Features

### 🎯 Core Capabilities
- **Natural Language Processing**: Ask questions about stocks in plain English
- **Real-time Stock Data**: Current prices, historical data, and market metrics
- **News Analysis**: Recent news aggregation and sentiment analysis
- **Price Movement Analysis**: Track price changes over various timeframes
- **Interactive Visualizations**: Candlestick charts, line graphs, and volume analysis
- **Multi-Agent Architecture**: Modular system with specialized agents

### 🤖 Core Logic (Implemented in Streamlit App, Mirrored in ADK Agents)

The core analytical functionalities, whether executed directly within the Streamlit app or by the conceptual ADK agents, include:

1.  **Ticker Identification**: Extracting stock symbols (e.g., "TSLA", "AAPL") from user queries.
2.  **News Retrieval**: Fetching recent news articles for a given stock ticker.
3.  **Price Fetching**: Getting current and historical stock prices.
4.  **Price Change Calculation**: Determining price fluctuations over various periods.
5.  **Data Synthesis & Analysis**: Combining news, price data, and sentiment to provide an analytical summary.

### 📊 Interface Modes

1. **Natural Language Query**: Ask questions like "Why did Tesla stock drop today?"
2. **Stock Data Visualization**: Interactive charts and technical analysis
3. **Manual Analysis**: Direct access to individual agent functions

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Alpha Vantage API key (free at [alphavantage.co](https://www.alphavantage.co/support/#api-key))

### Installation & Setup

1.  **Navigate to Project Directory**:
    Open your terminal or command prompt and change to the project's root directory:
    ```bash
    cd c:\Project\Intership_Test_AI_Agent
    ```

2.  **Create `.env` File for API Key**:
    *   In the project root (`c:\Project\Intership_Test_AI_Agent`), create a file named `.env`.
    *   Add your Alpha Vantage API key to this file. You can get a free key from [alphavantage.co](https://www.alphavantage.co/support/#api-key).
        ```env
        # c:\Project\Intership_Test_AI_Agent\.env
        ALPHA_VANTAGE_API_KEY="YOUR_ACTUAL_ALPHA_VANTAGE_API_KEY"
        ```
    *   Replace `YOUR_ACTUAL_ALPHA_VANTAGE_API_KEY` with your real key.

3.  **Run the Automated Setup and Launch Script (Recommended)**:
    This script will:
    *   Check your Python version.
    *   Install required packages from `requirements.txt` (if not already satisfied).
    *   Verify that the `.env` file and the API key are set up.
    *   Launch the Streamlit application (`unified_stock_analysis_app.py`).

    Execute the script:
    ```bash
    python setup_and_run.py
    ```

4.  **Manual Setup (Alternative)**:
    If you prefer to set up manually or if `setup_and_run.py` encounters issues:
    *   **Install Dependencies**: Open a terminal in the project root and run:
        ```bash
        pip install -r requirements.txt
        ```
    *   **Run the Streamlit Application**: After installing dependencies and setting up the `.env` file, run:
        ```bash
        streamlit run unified_stock_analysis_app.py
        ```

## Usage Examples

### Natural Language Queries
- "Why did Tesla stock drop today?"
- "What's happening with Palantir stock recently?"
- "How has Nvidia stock changed in the last 7 days?"
- "Show me Apple's current price and recent news"
- "What caused Amazon's stock movement this week?"

### Supported Stock Symbols
The system recognizes both company names and ticker symbols:
- **Company Names**: Tesla, Apple, Google, Microsoft, Amazon, etc.
- **Ticker Symbols**: TSLA, AAPL, GOOGL, MSFT, AMZN, etc.

## Technical Architecture

### System Architecture (Unified Application)

The `unified_stock_analysis_app.py` directly implements the logic for interacting with the Alpha Vantage API and presenting data. While it's not a multi-agent system in the ADK sense, it performs similar tasks in a monolithic but modular way within the Streamlit framework.

```
┌─────────────────────────────────────────────────────────────┐
│              Unified Streamlit Application                  │
│           (unified_stock_analysis_app.py)                 │
├─────────────────────────────────────────────────────────────┤
│  User Interface (Input Query, Select Mode, View Results)    │
├─────────────────────────────────────────────────────────────┤
│  Query Processing & Ticker Extraction Logic                 │
├─────────────────────────────────────────────────────────────┤
│  Data Fetching Functions (Price, News, Changes)             │
├─────────────────────────────────────────────────────────────┤
│  Data Analysis & Synthesis Logic                            │
├─────────────────────────────────────────────────────────────┤
│  Visualization Components (Plotly Charts, Metrics)          │
├─────────────────────────────────────────────────────────────┤
│                Alpha Vantage API (External)                 │
└─────────────────────────────────────────────────────────────┘
```

The `stock_analysis_adk/` directory provides a separate, conceptual multi-agent architecture using Google ADK for reference.

### Data Flow
1. **User Input**: Natural language query or direct ticker input
2. **Query Processing**: Extract ticker symbols and intent
3. **Agent Coordination**: Parallel execution of specialized agents
4. **Data Aggregation**: Combine results from all agents
5. **Analysis Generation**: Synthesize insights and recommendations
6. **Visualization**: Present results through interactive interface

## API Integration

### Alpha Vantage API
The system uses Alpha Vantage for:
- Real-time stock quotes
- Historical price data
- News and sentiment analysis
- Market fundamentals

### Rate Limits
- Free tier: 5 API requests per minute, 500 per day
- Premium tiers available for higher usage

## Project File Structure

```plaintext
c:\Project\Intership_Test_AI_Agent/
├── unified_stock_analysis_app.py  # Main Streamlit application (Primary entry point)
├── setup_and_run.py               # Script for easy setup and execution of the Streamlit app
├── requirements.txt                 # Python dependencies for the Streamlit application
├── README.md                        # This main project README file
├── PROJECT_STRUCTURE.md             # Document detailing the project's folder and file organization
├── PROJECT_SUMMARY.md               # Document summarizing the project's goals and outcomes
├── .env                             # Stores environment variables (e.g., ALPHA_VANTAGE_API_KEY)
├── .env.example                     # Example structure for the .env file
├── stock_analysis_adk/              # Directory for the Google ADK Multi-Agent System (Reference Implementation)
│   ├── README.md                    # Documentation specific to the ADK part
│   ├── requirements.txt             # Dependencies specific to the ADK agents
│   ├── .env                         # Environment variables for ADK agents (can be same as root .env)
│   ├── main_orchestrator_agent/     # Contains the main orchestrating ADK agent
│   │   ├── __init__.py
│   │   └── agent.py
│   └── sub_agents/                  # Contains specialized ADK sub-agents
│       ├── __init__.py
│       ├── identify_ticker_agent.py
│       ├── ticker_news_agent.py
│       ├── ticker_price_agent.py
│       ├── ticker_price_change_agent.py
│       └── ticker_analysis_agent.py
└── read.txt                         # Original task description (for reference)
```

## Features in Detail

### 🔍 Natural Language Processing
- Intelligent ticker extraction from conversational queries
- Context-aware timeframe detection (today, week, month)
- Support for company names and stock symbols
- Query intent classification

### 📈 Real-time Data Analysis
- Current stock prices with change indicators
- Historical price movements and trends
- Trading volume analysis
- 52-week high/low tracking

### 📰 News Integration
- Recent news aggregation from multiple sources
- Sentiment analysis of news articles
- Correlation between news events and price movements
- Source attribution and article links

### 📊 Interactive Visualizations
- **Candlestick Charts**: OHLC data with volume
- **Line Charts**: Price trends over time
- **Volume Charts**: Trading activity patterns
- **Metric Cards**: Key performance indicators

## Troubleshooting

### Common Issues

1. **API Key Error**:
   - Ensure `.env` file exists with valid `ALPHA_VANTAGE_API_KEY`
   - Check API key validity at Alpha Vantage dashboard

2. **Rate Limit Exceeded**:
   - Wait for rate limit reset (1 minute for free tier)
   - Consider upgrading to premium API plan

3. **No Data Found**:
   - Verify ticker symbol is correct
   - Check if market is open (some data only available during trading hours)

4. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Performance Optimization
- Use caching for frequently requested data
- Implement request batching for multiple queries
- Consider data persistence for historical analysis

## Future Enhancements

### Planned Features
- **Technical Indicators**: RSI, MACD, Moving Averages
- **Portfolio Tracking**: Multi-stock portfolio analysis
- **Alert System**: Price and news-based notifications
- **Machine Learning**: Predictive price modeling
- **Social Sentiment**: Twitter and Reddit sentiment analysis
- **Fundamental Analysis**: P/E ratios, earnings data

### Integration Opportunities
- **Additional Data Sources**: Yahoo Finance, IEX Cloud
- **Database Integration**: PostgreSQL, MongoDB for data persistence
- **Authentication**: User accounts and personalized dashboards
- **Mobile App**: React Native or Flutter implementation

## Contributing

This project demonstrates modern software architecture principles:
- **Modular Design**: Separate agents for different functionalities
- **API Integration**: External data source integration
- **User Experience**: Intuitive natural language interface
- **Scalability**: Extensible multi-agent framework

## License

This project is developed for educational and demonstration purposes. Please ensure compliance with Alpha Vantage API terms of service and any applicable financial data regulations.

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section above
2. Review Alpha Vantage API documentation
3. Ensure all dependencies are properly installed
4. Verify environment configuration

---

**Built with ❤️ using Streamlit, Google ADK Architecture, and Alpha Vantage API**