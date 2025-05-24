# Multi-Agent Stock Analysis System - Project Structure

## 📁 Project Overview

This project provides a comprehensive stock analysis system with two primary parts:

1.  **🚀 Unified Streamlit Application (`unified_stock_analysis_app.py`)**: The main, user-facing application for stock analysis.
2.  **🤖 Google ADK Multi-Agent System (`stock_analysis_adk/`)**: A reference implementation demonstrating a multi-agent architecture using Google's Agent Development Kit for similar stock analysis tasks.

## 🗂️ Directory Structure

```plaintext
c:\Project\Intership_Test_AI_Agent/
├── unified_stock_analysis_app.py  # Main Streamlit application (Primary entry point)
├── setup_and_run.py               # Script for easy setup and execution of the Streamlit app
├── requirements.txt                 # Python dependencies for the Streamlit application
├── README.md                        # Main project README file, high-level overview
├── PROJECT_STRUCTURE.md             # This file - detailed folder and file organization
├── PROJECT_SUMMARY.md               # Document summarizing the project's goals, features, and outcomes
├── .env                             # Stores environment variables (e.g., ALPHA_VANTAGE_API_KEY) for the unified app
├── .env.example                     # Example structure for the .env file
├── stock_analysis_adk/              # Directory for the Google ADK Multi-Agent System (Reference Implementation)
│   ├── README.md                    # Documentation specific to the ADK part
│   ├── requirements.txt             # Dependencies specific to the ADK agents
│   ├── .env                         # Environment variables for ADK agents (can be same as root .env or separate)
│   ├── main_orchestrator_agent/     # Contains the main orchestrating ADK agent
│   │   ├── __init__.py              # Makes the directory a Python package
│   │   └── agent.py                 # Defines the main orchestrator (root_agent)
│   └── sub_agents/                  # Contains specialized ADK sub-agents
│       ├── __init__.py              # Makes the directory a Python package
│       ├── identify_ticker_agent.py   # Agent to extract stock tickers from queries
│       ├── ticker_news_agent.py       # Agent to fetch news for a ticker
│       ├── ticker_price_agent.py      # Agent to get current/latest price for a ticker
│       ├── ticker_price_change_agent.py # Agent to calculate price changes
│       └── ticker_analysis_agent.py   # Agent to synthesize news and price data for analysis
└── read.txt                         # Original task description (for reference)
```

*Note: `__pycache__` directories are typically ignored by version control and are not listed.*

## 🎯 Component Descriptions

### 1. 🚀 **Unified Streamlit Application**
**Primary File**: `unified_stock_analysis_app.py`
**Setup & Run Script**: `setup_and_run.py`

**Purpose**: This is the main, production-ready application for end-users. It provides a comprehensive and interactive Streamlit interface for stock analysis.

**Key Features**:
-   **Natural Language Queries**: Users can ask questions about stocks in plain English (e.g., "What's the news on TSLA?", "Show me AAPL price chart").
-   **Multiple Analysis Modes**:
    *   *Natural Language Query Mode*: For conversational analysis.
    *   *Stock Data Visualization Mode*: For focused ticker data and charts.
    *   *Manual Analysis Mode*: Allows step-by-step invocation of analysis components (ticker ID, price, news, etc.).
-   **Interactive Visualizations**: Includes Plotly-based candlestick charts, line graphs for price trends, and volume bars.
-   **Real-time Data**: Fetches current stock prices, historical data, and company news using the Alpha Vantage API.
-   **News Sentiment**: Displays news articles and associated sentiment scores.
-   **Price Change Analysis**: Calculates and shows price changes over user-defined or preset timeframes.
-   **User-Friendly Setup**: The `setup_and_run.py` script automates dependency installation and application launch.

**Usage**: The recommended way to run is `python setup_and_run.py`. Alternatively, after manual setup: `streamlit run unified_stock_analysis_app.py`.

### 2. 🤖 **Google ADK Multi-Agent System (Reference Implementation)**
**Main Directory**: `stock_analysis_adk/`

**Purpose**: This section serves as a reference implementation of a multi-agent system built using the Google Agent Development Kit (ADK). It demonstrates how the stock analysis tasks performed by the unified application can be architected using distinct, coordinated agents. It is primarily for developers interested in ADK or multi-agent design patterns.

**Core Components**: (Located within `stock_analysis_adk/`)
- **Main Orchestrator** (`main_orchestrator_agent/agent.py`)
  - Coordinates all sub-agents
  - Handles query routing
  - Synthesizes final responses

- **Sub-Agents** (`sub_agents/`):
  - `identify_ticker_agent.py` - Extracts stock symbols
  - `ticker_news_agent.py` - Retrieves news data
  - `ticker_price_agent.py` - Fetches current prices
  - `ticker_price_change_agent.py` - Calculates price changes
  - `ticker_analysis_agent.py` - Synthesizes analysis

**Status**: This is a reference implementation. Running it requires familiarity with Google ADK, setting up the appropriate Python environment for ADK (see `stock_analysis_adk/requirements.txt`), and configuring API keys within its `.env` file or through your Google Cloud environment. The `main_orchestrator_agent/agent.py` contains an example `if __name__ == '__main__':` block for testing.



## 🔧 Configuration Files

### Environment Variables (`.env` files)
-   **`c:\Project\Intership_Test_AI_Agent\.env`**: The primary `.env` file for the **Unified Streamlit Application**. It must contain the `ALPHA_VANTAGE_API_KEY`.
-   **`c:\Project\Intership_Test_AI_Agent\stock_analysis_adk\.env`**: A separate `.env` file specifically for the **Google ADK Multi-Agent System**. This also requires `ALPHA_VANTAGE_API_KEY` and potentially other Google Cloud/Gemini related API keys if not using Application Default Credentials.
-   An `.env.example` file is provided in the root directory as a template.

### Python Dependencies (`requirements.txt` files)
-   **`c:\Project\Intership_Test_AI_Agent\requirements.txt`**: Contains all Python packages needed to run the **Unified Streamlit Application** (`unified_stock_analysis_app.py` and `setup_and_run.py`).
-   **`c:\Project\Intership_Test_AI_Agent\stock_analysis_adk\requirements.txt`**: Contains Python packages specific to the **Google ADK Multi-Agent System**, including `google-agent-toolbelt` (or similar ADK libraries) and `google-generativeai`.

## 🚀 How to Run

### 1. Unified Streamlit Application (Recommended for Users)
   - **Automated Setup & Launch**: 
     ```bash
     cd c:\Project\Intership_Test_AI_Agent
     python setup_and_run.py
     ```
   - **Manual Launch** (after installing dependencies from root `requirements.txt` and setting up root `.env`):
     ```bash
     cd c:\Project\Intership_Test_AI_Agent
     streamlit run unified_stock_analysis_app.py
     ```

### 2. Google ADK Multi-Agent System (For Developers/Reference)
   - Navigate to the ADK directory: 
     ```bash
     cd c:\Project\Intership_Test_AI_Agent\stock_analysis_adk
     ```
   - Ensure Python environment with ADK dependencies (from `stock_analysis_adk/requirements.txt`) is active.
   - Ensure `stock_analysis_adk/.env` is configured.
   - Run the main orchestrator agent (example from its `if __name__ == '__main__':` block):
     ```bash
     # From within stock_analysis_adk/main_orchestrator_agent/ directory
     python agent.py 
     # Or, from stock_analysis_adk/ directory as a module if paths are set up for it:
     # python -m main_orchestrator_agent.agent
     ```
   - *Note: Full ADK execution might involve `adk run` commands or specific deployment patterns not covered here.*

## 🎯 Primary Focus

-   The **Unified Streamlit Application (`unified_stock_analysis_app.py`)** is the polished, end-user-focused product of this project.
-   The **Google ADK Multi-Agent System (`stock_analysis_adk/`)** serves as a technical reference and a demonstration of an alternative (multi-agent) architectural approach to the same problem domain.

## 📝 Development Notes

-   The Unified Application implements the core logic (API calls, data processing, analysis) directly within its Python functions, structured for clarity and maintainability within the Streamlit framework.
-   The ADK system showcases how this logic can be distributed among specialized agents, which communicate and are orchestrated by a root agent. This is a more formal multi-agent pattern.
-   Both parts rely on the Alpha Vantage API for external data.

## 🔗 Alpha Vantage API Usage

Both the Unified Application and the ADK reference implementation utilize the Alpha Vantage API for:
-   Fetching current stock prices (`GLOBAL_QUOTE`).
-   Retrieving historical daily stock data (`TIME_SERIES_DAILY_ADJUSTED`).
-   Getting company news and sentiment (`NEWS_SENTIMENT`).

A free API key has rate limits (e.g., 25 requests per day as of recent checks, but verify on their site). Ensure your `.env` file(s) are correctly configured with your key.

---

**Last Updated**: Project structure and documentation finalized.
**Primary Application**: `unified_stock_analysis_app.py` (run via `python setup_and_run.py`).