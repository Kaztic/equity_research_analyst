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

# --- Agent 1: Data Fetching Agent ---
async def fetch_financial_data(session: ClientSession, ticker: str) -> dict:
    """
    Agent 1: Fetches financial data using the MCP tool.
    """
    logging.info(f"[Agent 1] Fetching financial data for ticker: {ticker}...")
    try:
        result = await session.call_tool("get_stock_fundamentals", {"ticker": ticker})
        
        # Standardize result processing
        if hasattr(result, 'content') and result.content and isinstance(result.content, list):
            stock_data_str = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
            stock_data = json.loads(stock_data_str)
        else:
            stock_data = result if isinstance(result, dict) else {}

        # Validate the data
        if not stock_data or stock_data.get("marketCap") == "N/A":
            error_message = f"Could not retrieve valid financial data for '{ticker}'."
            logging.warning(f"[Agent 1] {error_message}")
            return {"error": error_message}
            
        logging.info(f"[Agent 1] Data fetched successfully for: {stock_data.get('companyName')}")
        return stock_data

    except Exception as e:
        logging.error(f"[Agent 1] Error fetching data: {e}", exc_info=True)
        return {"error": f"An error occurred while fetching data: {e}"}

# --- Agent 2: Financial Analyst Agent ---
async def analyze_financial_metrics(stock_data: dict) -> str:
    """
    Agent 2: Analyzes the fetched financial data and generates a structured report.
    """
    logging.info("[Agent 2] Generating financial analysis with Google Gemini...")
    model = GenerativeModel(model_name="gemini-1.5-flash")
    
    prompt = f"""
    You are a professional Equity Research Analyst. Your task is to perform a fundamental analysis based on the provided data.
    Do not add any introductory or concluding sentences outside of the requested structure.

    **Financial Data:**
    ```json
    {json.dumps(stock_data, indent=2)}
    ```

    **Generate the report using this exact Markdown structure:**

    ### Company Overview
    - **Company Name:** {stock_data.get("companyName", "N/A")}
    - **Business Summary:** Briefly describe the company's business based on the provided summary.

    ### Key Financial Metrics Analysis
    - **Market Capitalization:** Analyze its significance as an indicator of the company's size.
    - **Valuation Ratios (P/E & P/B):** Explain the Trailing P/E, Forward P/E, and Price-to-Book ratios.
    - **Dividend Yield:** Discuss the dividend yield and its implications for income-focused investors.
    - **Stock Performance:** Comment on the 52-week high and low to describe its recent price range.
    """
    
    response = await model.generate_content_async(prompt)
    logging.info("[Agent 2] Financial analysis generated successfully.")
    return response.text

# --- Agent 3: Investment Advisor Agent ---
async def provide_investment_outlook(analysis: str) -> str:
    """
    Agent 3: Provides a high-level summary, outlook, and disclaimer based on the analysis.
    """
    logging.info("[Agent 3] Generating investment summary and outlook...")
    model = GenerativeModel(model_name="gemini-1.5-flash")
    
    prompt = f"""
    You are a senior Investment Advisor. Your task is to provide a balanced summary and a forward-looking statement based on the financial analysis report.
    Do not repeat the detailed metrics from the report.

    **Analyst's Report:**
    ---
    {analysis}
    ---

    **Generate the final sections using this exact Markdown structure:**

    ### Investment Summary & Outlook
    - Provide a neutral, balanced summary of the company's financial health based *only* on the provided analysis.
    - Highlight potential strengths and weaknesses evident from the metrics.
    - Conclude with a brief, forward-looking statement about what an investor might watch for.

    ### Disclaimer
    - Add a standard disclaimer: "This analysis is for informational and educational purposes only and does not constitute financial advice. Investors should conduct their own research before making any investment decisions."
    """
    
    response = await model.generate_content_async(prompt)
    logging.info("[Agent 3] Investment outlook generated successfully.")
    return response.text

# --- Main Orchestrator ---
async def run_equity_research_async(ticker: str) -> str:
    """
    Orchestrates the multi-agent system to perform equity research.
    """
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable is not set."

    # --- Setup MCP Client ---
    server_params = StdioServerParameters(command="python", args=["server.py"])
    
    logging.info("Orchestrator: Initializing agent workflow...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # --- Step 1: Call Data Fetching Agent ---
            stock_data = await fetch_financial_data(session, ticker)
            if stock_data.get("error"):
                return stock_data["error"]

            # --- Step 2: Call Financial Analyst Agent ---
            financial_analysis = await analyze_financial_metrics(stock_data)

            # --- Step 3: Call Investment Advisor Agent ---
            investment_outlook = await provide_investment_outlook(financial_analysis)
            
            # --- Step 4: Combine outputs for the final report ---
            final_report = f"{financial_analysis}\n\n{investment_outlook}"
            logging.info("Orchestrator: Agent workflow completed successfully.")
            return final_report

    return "Orchestrator: Failed to complete the workflow."


# --- Synchronous Wrapper for Streamlit ---
def run_equity_research(ticker: str) -> str:
    """
    Synchronous wrapper to run the async orchestrator from Streamlit.
    """
    try:
        return asyncio.run(run_equity_research_async(ticker))
    except Exception as e:
        logging.error(f"Failed to execute the asyncio event loop: {e}", exc_info=True)
        return f"A critical application error occurred: {e}"