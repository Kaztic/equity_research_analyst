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

# Load environment variables
load_dotenv()

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Agent 1: Quantitative Analyst Agent ---
async def quantitative_analyst_agent(session: ClientSession, ticker: str) -> dict:
    """
    Agent 1: Fetches and processes all numerical data.
    """
    logging.info(f"[Quantitative Agent] Starting numerical analysis for {ticker}...")
    try:
        # Fetch fundamental data and historical trends in parallel
        fundamentals_task = session.call_tool("get_stock_fundamentals", {"ticker": ticker})
        historical_task = session.call_tool("get_historical_financials", {"ticker": ticker})
        
        results = await asyncio.gather(fundamentals_task, historical_task)
        
        fundamentals = results[0].content[0].text if hasattr(results[0], 'content') else results[0]
        historical_data = results[1].content[0].text if hasattr(results[1], 'content') else results[1]

        # Convert string results to dictionaries
        fundamentals = json.loads(fundamentals) if isinstance(fundamentals, str) else fundamentals
        historical_data = json.loads(historical_data) if isinstance(historical_data, str) else historical_data

        if "error" in fundamentals or "error" in historical_data:
            error_msg = fundamentals.get("error") or historical_data.get("error")
            logging.error(f"[Quantitative Agent] Failed to fetch data: {error_msg}")
            return {"error": f"Data fetching failed: {error_msg}"}

        logging.info("[Quantitative Agent] Numerical data fetched successfully.")
        return {
            "fundamentals": fundamentals,
            "historical_data": historical_data
        }

    except Exception as e:
        logging.error(f"[Quantitative Agent] Error during analysis: {e}", exc_info=True)
        return {"error": f"An unexpected error occurred in the Quantitative Agent: {e}"}

# --- Agent 2: Qualitative Analyst Agent ---
async def qualitative_analyst_agent(session: ClientSession, company_name: str, sector: str) -> str:
    """
    Agent 2: Gathers and synthesizes market sentiment and industry news.
    """
    logging.info(f"[Qualitative Agent] Starting market research for {company_name}...")
    try:
        # Perform targeted Google searches in parallel
        news_query = f"latest news and analyst ratings for {company_name}"
        industry_query = f"outlook and trends for the {sector} sector 2025"
        
        news_task = session.call_tool("perform_google_search", {"query": news_query})
        industry_task = session.call_tool("perform_google_search", {"query": industry_query})
        
        results = await asyncio.gather(news_task, industry_task)
        
        news_results = results[0].content[0].text if hasattr(results[0], 'content') else results[0]
        industry_results = results[1].content[0].text if hasattr(results[1], 'content') else results[1]

        # Use an LLM to synthesize the search results
        model = GenerativeModel(model_name="gemini-2.0-flash")
        prompt = f"""
        You are a Market Research Analyst. Your task is to synthesize the provided search results into a concise summary for an investment report.
        Focus on the overall sentiment, key growth drivers, challenges, and the competitive landscape.

        **Recent News & Analyst Ratings (Search Results):**
        {news_results}

        **Industry Outlook & Trends (Search Results):**
        {industry_results}

        **Synthesized Summary:**
        Based on the information above, please provide a brief report covering:
        1.  **Market Sentiment:** What is the general feeling about the company (e.g., bullish, bearish, neutral)? Mention any recent analyst upgrades or downgrades.
        2.  **Industry Health:** Is the industry expected to grow, shrink, or remain stable? What are the key trends (e.g., AI adoption, regulatory changes, supply chain issues)?
        """
        
        response = await model.generate_content_async(prompt)
        logging.info("[Qualitative Agent] Market research summary generated.")
        return response.text

    except Exception as e:
        logging.error(f"[Qualitative Agent] Error during analysis: {e}", exc_info=True)
        return f"An error occurred in the Qualitative Agent: {e}"

# --- Agent 3: Synthesis & Reporting Agent ---
async def synthesis_reporting_agent(quantitative_data: dict, qualitative_analysis: str) -> str:
    """
    Agent 3: Combines all data into a final, user-friendly report.
    """
    logging.info("[Synthesis Agent] Generating final comprehensive report...")
    model = GenerativeModel(model_name="gemini-2.0-flash")
    
    prompt = f"""
    You are a Senior Investment Analyst creating a report for a retail investor. Your goal is to be clear, insightful, and easy to understand.
    Use the provided Quantitative Data and Qualitative Analysis to generate a comprehensive report. **Explain what the data MEANS in simple terms.**

    **Quantitative Data:**
    ```json
    {json.dumps(quantitative_data, indent=2)}
    ```

    **Qualitative Analysis & Market Research:**
    ---
    {qualitative_analysis}
    ---

    **Generate the full report using this exact Markdown structure:**

    # Comprehensive Analysis for {quantitative_data['fundamentals'].get('companyName')} ({quantitative_data['fundamentals'].get('ticker')})

    ## 📊 At-a-Glance Scorecard
    *   **Valuation:** (e.g., Appears Undervalued/Fairly Valued/Overvalued compared to earnings and assets.)
    *   **Financial Health:** (e.g., Strong/Moderate/Weak based on debt and profitability.)
    *   **Growth:** (e.g., Strong/Stable/Declining sales and earnings trends.)
    *   **Market Sentiment:** (e.g., Positive/Neutral/Negative based on news and industry outlook.)

    ## 📝 Executive Summary
    - Provide a 3-4 sentence summary of the key takeaways from the entire analysis. Start with the company's market position and conclude with the primary risks and opportunities.

    ## 🏢 Company & Industry Overview
    - **Business Model:** Briefly summarize the company's business based on the 'longBusinessSummary'.
    - **Industry Context:** Briefly describe the industry outlook based on the qualitative analysis.

    ## 📈 Financial Performance & Health
    - **Historical Trends:** Analyze the 3-year trend for Revenue and Net Income. Is the company growing? Is it consistently profitable?
    - **Profitability:** Explain Return on Equity (ROE) and what the current figure means for shareholder value.
    - **Debt Analysis:** Explain the Debt-to-Equity ratio. Is the company's debt level a concern?

    ## 💰 Valuation Analysis
    - **P/E Ratios:** Explain the Trailing and Forward P/E ratios in simple terms. Is the stock cheap or expensive relative to its own earnings?
    - **P/B Ratio:** Explain the Price-to-Book ratio. What does it suggest about how the market values the company's assets?

    ## 🔍 Investment Thesis: Strengths & Risks
    - **Potential Strengths (Bull Case):**
        - (List 2-3 key strengths based on all available data, e.g., market leadership, strong profitability, high institutional ownership.)
    - **Potential Risks (Bear Case):**
        - (List 2-3 key risks, e.g., high valuation, industry headwinds, high debt, poor recent performance.)

    ## Disclaimer
    - Add a standard disclaimer: "This AI-generated analysis is for informational purposes only and not financial advice. Always conduct your own research."
    """
    response = await model.generate_content_async(prompt)
    logging.info("[Synthesis Agent] Final report generated successfully.")
    return response.text

# --- Main Orchestrator ---
async def run_equity_research_async(ticker: str) -> str:
    """
    Orchestrates the new multi-agent system to perform enhanced equity research.
    """
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable is not set."

    server_params = StdioServerParameters(command="python", args=["server.py"])
    
    logging.info("--- Orchestrator: Starting Workflow ---")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Step 1: Call Quantitative Agent
            quantitative_data = await quantitative_analyst_agent(session, ticker)
            if "error" in quantitative_data:
                return quantitative_data["error"]

            company_name = quantitative_data['fundamentals'].get('companyName', ticker)
            sector = quantitative_data['fundamentals'].get('sector', 'technology')

            # Step 2: Call Qualitative Agent
            qualitative_analysis = await qualitative_analyst_agent(session, company_name, sector)
            if "error" in qualitative_analysis:
                return qualitative_analysis # Return error if qualitative analysis fails

            # Step 3: Call Synthesis & Reporting Agent
            final_report = await synthesis_reporting_agent(quantitative_data, qualitative_analysis)
            
            logging.info("--- Orchestrator: Workflow Completed Successfully ---")
            return final_report

    return "Orchestrator: Failed to complete the workflow."

# Synchronous Wrapper for Streamlit ---
def run_equity_research(ticker: str) -> str:
    try:
        return asyncio.run(run_equity_research_async(ticker))
    except Exception as e:
        logging.error(f"Failed to execute the asyncio event loop: {e}", exc_info=True)
        return f"A critical application error occurred: {e}"