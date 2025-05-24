from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# This agent will primarily use its LLM capabilities to analyze
# data provided to it by other agents (news, price changes).
# For this example, we'll define a simple tool that structures the input,
# but the core analysis is done by the LLM based on its instructions.

def structure_analysis_input(ticker: str, news_items: list, price_change_data: dict) -> dict:
    """Structures the input for the ticker analysis agent.

    Args:
        ticker (str): The stock ticker symbol.
        news_items (list): A list of news items (dictionaries with title, summary, etc.).
        price_change_data (dict): A dictionary containing price change information 
                                  (percentage_change, timeframe_description, etc.).

    Returns:
        dict: A structured dictionary of the input data for the LLM to process.
    """
    return {
        "status": "success",
        "ticker": ticker,
        "news": news_items,
        "price_change": price_change_data
    }

# The analysis itself will be performed by the LLM within the agent based on its prompt/instruction.
# If more complex, non-LLM analysis steps were needed, they could be separate tools.

ticker_analysis_input_tool = FunctionTool(
    structure_analysis_input
)

ticker_analysis_agent = Agent(
    name="ticker_analysis_sub_agent",
    model="gemini-1.5-pro", # Using a more capable model for analysis might be beneficial
    description="A sub-agent that analyzes and summarizes the reasons behind recent stock price movements using news and historical price data.",
    instruction=(
        "You are a financial analyst agent. Your task is to analyze the provided stock ticker, recent news, and price change data. "
        "Explain the potential reasons behind the stock's recent price movements. "
        "Consider the sentiment of the news, the magnitude of the price change, and the timeframe. "
        "Provide a concise summary. If news is unavailable or the price change is minimal, state that. "
        "Input will be structured by the 'structure_analysis_input_tool'."
        "Focus on connecting news events to price movements if possible."
        "Output should be a textual summary of your analysis."
    ),
    tools=[ticker_analysis_input_tool] # The LLM will use the output of this tool as its context
)