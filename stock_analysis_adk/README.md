# Stock Analysis Multi-Agent System (Google ADK)

This project implements a multi-agent system using the Google Agent Development Kit (ADK) to perform stock analysis based on natural language queries. It can identify stock tickers, fetch current stock prices, retrieve recent news articles, calculate price changes over various timeframes, and synthesize this information into a coherent analysis of potential reasons behind stock movements.

## Project Structure

```
stock_analysis_adk/
├── main_orchestrator_agent/      # Directory for the main coordinating agent
│   ├── __init__.py             # Makes the directory a Python package
│   └── agent.py                # Defines the main orchestrator (root_agent)
├── sub_agents/                   # Directory for specialized sub-agents
│   ├── __init__.py             # Makes the directory a Python package
│   ├── identify_ticker_agent.py  # Agent to extract stock tickers from queries
│   ├── ticker_news_agent.py      # Agent to fetch news for a ticker
│   ├── ticker_price_agent.py     # Agent to get current/latest price for a ticker
│   ├── ticker_price_change_agent.py # Agent to calculate price changes
│   └── ticker_analysis_agent.py  # Agent to synthesize news and price data for analysis
├── .env                          # Centralized environment variables (e.g., API keys)
├── requirements.txt              # Python dependencies for the ADK agents
└── README.md                     # This documentation file
```

**Note:** The `.env` file is now located at the root of the `stock_analysis_adk` directory for centralized access by all agents. The `main_orchestrator_agent/agent.py` and all sub-agents have been updated to load the `.env` file from this common location.

## Setup

1.  **Clone the repository (if applicable) or ensure you have the `stock_analysis_adk` directory.**

2.  **Create and configure the environment file:**
    *   Navigate to the root of the `stock_analysis_adk/` directory.
    *   Create a file named `.env` (e.g., by copying from `.env.example` if provided, or creating a new one).
    *   Add your Alpha Vantage API key to this `.env` file:
        ```env
        # stock_analysis_adk/.env
        ALPHA_VANTAGE_API_KEY="YOUR_ALPHA_VANTAGE_API_KEY"
        
        # Optional: If using Google Vertex AI for Gemini models directly via API key (ADK might handle this differently)
        # GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY" 
        # or specific Vertex AI credentials as per Google ADK documentation.
        ```
    *   Replace `"YOUR_ALPHA_VANTAGE_API_KEY"` with your actual Alpha Vantage API key. You can obtain a free key from the [Alpha Vantage website](https://www.alphavantage.co/support/#api-key).
    *   The agents are configured to use Google's `gemini-1.5-flash` or `gemini-1.5-pro` models. Ensure your Google Cloud environment is set up correctly for ADK and these models, or that necessary API keys (like `GOOGLE_API_KEY` for direct Gemini API access if not using Vertex AI through ADK's default mechanisms) are configured if required by your ADK setup. The ADK typically handles authentication with Google services if run within a properly configured Google Cloud environment or if application default credentials are set up.

3.  **Install dependencies:**
    *   Navigate to the root of the `stock_analysis_adk` directory.
    *   Create a virtual environment (recommended):
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```
    *   Install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

## Running the System

This project is built with Google ADK. The primary way to run and interact with ADK agents is typically through the `adk` command-line tool or by integrating them into a larger application (e.g., a web service).

1.  **Using `adk run` (Conceptual - requires ADK CLI to be installed and configured):**
    The `main_orchestrator_agent/agent.py` file contains a `root_agent`. You would typically run this agent using the ADK CLI.

    ```bash
    # Ensure your environment (including API keys from .env) is loaded
    # and you are in a directory where the ADK can find your agent modules.
    # The exact command might vary based on your ADK setup and how you register agents.

    # Example: Running with a query (this is a conceptual command)
    # adk run stock_analysis_adk.main_orchestrator_agent --query "What is the latest news for TSLA?"
    ```

2.  **Programmatic Execution (Example):**
    The `main_orchestrator_agent/agent.py` includes a commented-out `if __name__ == '__main__':` block that demonstrates how to run the agent programmatically using `InMemoryRunner`. You can uncomment and adapt this for testing:

    ```python
    # In stock_analysis_adk/main_orchestrator_agent/agent.py
    # ... (rest of the agent code)

    if __name__ == '__main__':
        from google.adk.runner import InMemoryRunner
        from google.adk.events import Event
        import os
        from dotenv import load_dotenv

        # Load environment variables from .env in the same directory
        load_dotenv()

        # Verify API key is loaded (optional check)
        # print(f"Alpha Vantage Key Loaded: {os.getenv('ALPHA_VANTAGE_API_KEY') is not None}")

        runner = InMemoryRunner()
        query = "Why did Tesla stock drop today?"
        print(f"\n--- Running query: {query} ---")
        response = runner.run_agent_once(agent=root_agent, initial_event=Event(text_content=query))
        print(f"Response to '{query}':\n{response.text_content}")
    ```
    To run this example, navigate to the `stock_analysis_adk/main_orchestrator_agent/` directory and execute `python agent.py`.
    Ensure that the `.env` file is present in the parent `stock_analysis_adk/` directory, as the script is configured to load it from there.

    **Note on Running the Example:**
    The `agent.py` script in `main_orchestrator_agent` is designed to be run directly for testing (i.e., `python agent.py` from within its directory). It handles `PYTHONPATH` adjustments internally to correctly import sub-agents from the sibling `sub_agents` directory and load the `.env` file from its parent directory (`stock_analysis_adk`).

    If you prefer to run it as a module from the `stock_analysis_adk` root directory (e.g., `python -m main_orchestrator_agent.agent`), this should also work due to the `__init__.py` files making the directories packages. The internal path adjustments in `agent.py` are robust enough to handle both scenarios.

## How it Works

The `root_agent` (defined in `main_orchestrator_agent/agent.py`) acts as the central coordinator. When it receives a natural language query, it delegates tasks to specialized sub-agents, which are configured as its tools:

1.  **`identify_ticker_agent`**: This sub-agent is responsible for parsing the user's query to extract relevant stock ticker symbols (e.g., "AAPL", "TSLA"). It uses a combination of keyword matching and LLM capabilities.
2.  **`ticker_price_agent`**: Once a ticker is identified, this sub-agent fetches the latest available stock price (current or last closing) from the Alpha Vantage API. It includes details like open, high, low, and volume.
3.  **`ticker_news_agent`**: This sub-agent retrieves recent news articles related to the identified stock ticker from the Alpha Vantage API. It provides summaries and sentiment if available.
4.  **`ticker_price_change_agent`**: This sub-agent calculates the stock's price change over various predefined or specified timeframes (e.g., "today", "past 7 days", "past month") using historical data from Alpha Vantage.
5.  **`ticker_analysis_agent` (now `ticker_synthesis_and_analysis_sub_agent`)**: This sub-agent takes the structured data (current price, news, price changes) gathered by the other agents and uses its LLM (e.g., `gemini-1.5-pro`) to synthesize this information. It generates a textual analysis explaining potential reasons for the stock's recent performance, correlating news events with price movements.

The `root_agent` manages the flow of information between these sub-agents and compiles their outputs to form a comprehensive answer to the user's original query.

## Key Dependencies

*   **`google-agent-toolbelt` (or `google-adk`)**: The core Google Agent Development Kit library. (Note: The exact package name might vary based on the ADK version; ensure you have the correct one installed for your ADK environment).
*   **`python-dotenv`**: For loading environment variables (like API keys) from the `.env` file.
*   **`requests`**: Used by sub-agents to make HTTP requests to the Alpha Vantage API for stock data and news.
*   **`google-generativeai`**: Provides access to Google's Gemini models, which are used by the agents for natural language understanding, generation, and analysis.
*   **`google-cloud-aiplatform`**: Often a dependency for ADK, especially when integrating with Vertex AI services.

For a complete and precise list of dependencies and their versions, please refer to the `stock_analysis_adk/requirements.txt` file.