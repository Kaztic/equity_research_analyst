# main.py

import os
import json
import logging
import asyncio
import google.generativeai as genai
from google.generativeai import GenerativeModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Set up basic logging to see the agent's progress in the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- Asynchronous Core Function ---

async def run_equity_research_async(ticker: str) -> str:
    """
    Asynchronously orchestrates the multi-agent system to perform equity research.
    """
    # Configure the Google Gemini API
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: Your GOOGLE_API_KEY environment variable is not set. Please set it to run the analysis."

    try:
        # Initialize the MCP client and connect to the FastMCP server
        logging.info("Initializing MCP client and starting the data server...")
        
        server_params = StdioServerParameters(
            command="python",
            args=["server.py"],
            env=None
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                logging.info("MCP client connected successfully.")
                
                # Call the tool
                logging.info(f"[Agent 1] Fetching financial data for ticker: {ticker}...")
                result = await session.call_tool("get_stock_fundamentals", {"ticker": ticker})
                
                # Extract the content from the result
                if hasattr(result, 'content') and result.content:
                    # The content might be a list of content blocks or a dict
                    if isinstance(result.content, list) and len(result.content) > 0:
                        # If it's a list, get the first item's text
                        stock_data = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                        try:
                            # Try to parse as JSON if it's a string
                            stock_data = json.loads(stock_data) if isinstance(stock_data, str) else stock_data
                        except json.JSONDecodeError:
                            pass
                    else:
                        stock_data = result.content
                else:
                    # Fallback to checking for a direct result
                    stock_data = result
                
                logging.info(f"Raw result from MCP tool: {result}")
                logging.info(f"Processed stock_data: {stock_data}")
                
                # Validate the data returned from the tool
                if not stock_data or (isinstance(stock_data, dict) and stock_data.get("marketCap") == "N/A"):
                    error_message = f"Could not retrieve valid financial data for '{ticker}'. Please ensure it is a valid stock ticker and try again."
                    logging.warning(f"[Agent 1] {error_message}")
                    return error_message

                logging.info(f"[Agent 1] Data fetched successfully: {stock_data.get('companyName') if isinstance(stock_data, dict) else 'Unknown'}")

        # --- Agent 2: Equity Research Analyst (AI Analysis) ---
        logging.info("[Agent 2] Generating analysis with Google Gemini 1.5 Flash...")
        model = GenerativeModel(model_name="gemini-1.5-flash")

        # This detailed prompt guides the Gemini model to act as the research analyst agent
        prompt = f"""
        You are a professional Equity Research Analyst. Your task is to generate a clear, concise, and insightful
        fundamental analysis report for the company with the ticker '{stock_data.get("ticker") if isinstance(stock_data, dict) else ticker}'.

            Use the following financial data to structure your report:
            ```json
            {json.dumps(stock_data, indent=2)}
            ```

            **Please create the report using the following structure in Markdown format:**

            ### 1. 🏢 Company Overview
            - Start with the company name.
            - Briefly summarize the business based on the 'longBusinessSummary'.

            ### 2. 📊 Key Financial Metrics Analysis
            - **Market Capitalization:** Explain its significance as an indicator of the company's size.
            - **Valuation Ratios (P/E & P/B):** Analyze the Trailing P/E, Forward P/E, and Price-to-Book ratios. Explain what each one indicates about the company's current valuation.
            - **Dividend Yield:** Discuss the dividend yield and what it implies for investors seeking income.
            - **Stock Performance:** Comment on the 52-week high and low to give a sense of its recent volatility and price range.

            ### 3. 📝 Investment Summary & Outlook
            - Provide a neutral, balanced summary of the company's financial health based *only* on the provided data.
            - Highlight potential strengths (e.g., strong market position, profitability) and weaknesses or risks (e.g., high valuation, no dividend) evident from the metrics.
            - Conclude with a brief, a forward-looking statement about what an investor might want to watch for.

            ### 4. ⚠️ Disclaimer
            - Add a standard disclaimer stating that this analysis is not financial advice and is for informational and educational purposes only.

        Generate the report now.
        """

        response = model.generate_content(prompt)
        analysis_text = response.text
        logging.info("[Agent 2] Analysis generated successfully.")

        return analysis_text

    except Exception as e:
        logging.error(f"An unexpected error occurred during the analysis process: {e}", exc_info=True)
        return f"An error occurred during the analysis process: {e}"

# --- Synchronous Wrapper for Streamlit ---

def run_equity_research(ticker: str) -> str:
    """
    This is the synchronous wrapper function that Streamlit calls.
    It runs the main async logic and returns the result.
    """
    try:
        # Use asyncio.run() to execute the async function and wait for its result
        return asyncio.run(run_equity_research_async(ticker))
    except Exception as e:
        # Catch potential errors from the event loop itself
        logging.error(f"Failed to execute the asyncio event loop: {e}", exc_info=True)
        return f"A critical application error occurred: {e}"