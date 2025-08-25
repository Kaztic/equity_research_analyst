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

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Agent 1: Financial Data Engine Agent ---
async def financial_data_engine_agent(session: ClientSession, ticker: str) -> dict:
    """Fetches all raw numerical data."""
    logging.info(f"[Data Engine] Fetching comprehensive financial data for {ticker}...")
    result = await session.call_tool("get_comprehensive_financial_data", {"ticker": ticker})
    data = json.loads(result.content[0].text) if hasattr(result, 'content') else result
    if "error" in data:
        logging.error(f"[Data Engine] Failed: {data['error']}")
    else:
        logging.info("[Data Engine] Successfully fetched all financial data.")
    return data

# --- Agent 2: Market Intelligence Agent ---
async def market_intelligence_agent(session: ClientSession, company_name: str, sector: str) -> str:
    """Gathers and synthesizes qualitative market data."""
    logging.info(f"[Market Intelligence] Gathering qualitative data for {company_name}...")
    queries = {
        "news": f"latest news and analyst sentiment for {company_name}",
        "industry": f"Porter's Five Forces analysis for the {sector} industry",
        "transcripts": f"latest earnings call transcript summary for {company_name}"
    }
    
    tasks = [session.call_tool("perform_google_search", {"query": q}) for q in queries.values()]
    results = await asyncio.gather(*tasks)

    search_data = {key: (res.content[0].text if hasattr(res, 'content') else res) for key, res in zip(queries.keys(), results)}
    
    model = GenerativeModel(model_name="gemini-1.5-pro-latest")
    prompt = f"""
    As a Market Intelligence Analyst, synthesize the following search results into a concise qualitative report.

    **Recent News & Sentiment:**
    {search_data['news']}

    **Industry Competitive Landscape (Porter's Five Forces):**
    {search_data['industry']}

    **Earnings Call Insights:**
    {search_data['transcripts']}

    **Synthesized Report:**
    1.  **Executive Sentiment & Key Themes:** Based on the earnings call, what is management's tone (confident, cautious)? What are the key strategic focus areas?
    2.  **SWOT Analysis:** Based on all data, provide a brief SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis.
    3.  **Market Position (Porter's Analysis):** Briefly analyze the company's competitive standing within its industry based on the search results.
    """
    response = await model.generate_content_async(prompt)
    logging.info("[Market Intelligence] Successfully synthesized qualitative data.")
    return response.text

# --- Agent 3: Valuation Modeling Agent ---
async def valuation_modeling_agent(session: ClientSession, financial_data: dict) -> dict:
    """Performs DCF and Monte Carlo simulations."""
    logging.info("[Valuation Modeler] Running DCF and Monte Carlo simulations...")
    result = await session.call_tool("perform_dcf_and_monte_carlo", {"financial_data": financial_data})
    data = json.loads(result.content[0].text) if hasattr(result, 'content') else result
    if "error" in data:
        logging.error(f"[Valuation Modeler] Failed: {data['error']}")
    else:
        logging.info("[Valuation Modeler] Financial models generated successfully.")
    return data

# --- Agent 4: Strategic Synthesis Agent ---
async def strategic_synthesis_agent(financial_data: dict, market_analysis: str, valuation_models: dict) -> str:
    """Combines all analyses into a professional-grade investment thesis."""
    logging.info("[Chief Analyst] Synthesizing all data into the final report...")
    model = GenerativeModel(model_name="gemini-1.5-pro-latest")
    
    prompt = f"""
    As a Senior Equity Research Analyst, create a state-of-the-art investment report. Integrate the provided quantitative data, market intelligence, and valuation models into a cohesive, professional thesis.

    **1. Raw Financial & Ownership Data:**
    ```json
    {json.dumps(financial_data['info'], indent=2)}
    ```

    **2. Qualitative Market Intelligence Report:**
    ---
    {market_analysis}
    ---

    **3. Intrinsic Value Modeling Results:**
    ```json
    {json.dumps(valuation_models, indent=2)}
    ```

    **Generate the Final Report using this exact structure:**

    # Professional Equity Research Report: {financial_data['info'].get('shortName')} ({financial_data['info'].get('ticker')})

    ## 1. Executive Summary & Investment Thesis
    - **Thesis:** Start with a one-sentence investment thesis (e.g., "We rate [Company] a 'Buy' due to its durable competitive advantages and undervalued status...").
    - **Valuation Summary:** State the current price vs. the calculated intrinsic value from the DCF and Monte Carlo models.
    - **Key Drivers:** List 2-3 key factors that support the thesis.
    - **Primary Risks:** List 2-3 primary risks that could invalidate the thesis.

    ## 2. Intrinsic Value Analysis (DCF & Monte Carlo)
    - **Base Case DCF:** Explain the intrinsic value calculated from the base-case DCF. Compare this to the current stock price.
    - **Probabilistic Valuation (Monte Carlo):** Explain the valuation range (25th-75th percentile) from the Monte Carlo simulation. State the median value and what the range implies about valuation uncertainty.
    - **Valuation Verdict:** Based on the models, conclude whether the stock appears Undervalued, Fairly Valued, or Overvalued.

    ## 3. Strategic & Qualitative Analysis
    - **Business Moat (Competitive Advantage):** Based on the SWOT and Porter's analysis, what is the source and strength of the company's competitive advantage?
    - **Management Outlook:** What was the tone and focus of the latest earnings call? Are there any forward-looking statements of note?
    - **Institutional Conviction:** Comment on the percentage of shares held by institutions. Is this high or low for its sector?

    ## 4. Financial Health & Performance
    - **Profitability & Efficiency:** Analyze Return on Equity (ROE) and Debt-to-Equity. Is the company generating strong returns on its capital? Is its debt manageable?
    - **Growth Trajectory:** Briefly comment on the historical revenue and earnings growth rates. Does this support the assumptions used in the DCF model?

    ## 5. Risk Analysis
    - **Bear Case:** Elaborate on the primary risks. What internal or external factors could cause the stock to underperform?
    - **Insider Activity:** Briefly mention if there have been any significant insider transactions (buying or selling) as a potential signal.

    ## 6. Disclaimer
    - This report is an AI-generated analysis based on public data and simplified financial models. It is not financial advice. All investment decisions should be made with a qualified financial professional after conducting personal due diligence. The assumptions used in the DCF model may not reflect future reality.
    """
    response = await model.generate_content_async(prompt)
    logging.info("[Chief Analyst] Final report generation complete.")
    return response.text

# --- Main Orchestrator ---
async def run_equity_research_async(ticker: str) -> str:
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable is not set."

    server_params = StdioServerParameters(command="python", args=["server.py"])
    
    logging.info(f"--- Orchestrator: Initiating multi-agent workflow for {ticker} ---")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Agent 1: Fetch Data
            financial_data = await financial_data_engine_agent(session, ticker)
            if "error" in financial_data: return f"Workflow failed at Data Engine: {financial_data['error']}"

            # Agent 2 & 3: Run in parallel
            market_intel_task = market_intelligence_agent(session, financial_data['info'].get('shortName', ticker), financial_data['info'].get('sector', ''))
            valuation_model_task = valuation_modeling_agent(session, financial_data)
            market_analysis, valuation_models = await asyncio.gather(market_intel_task, valuation_model_task)
            
            if "error" in valuation_models: return f"Workflow failed at Valuation Modeler: {valuation_models['error']}"

            # Agent 4: Synthesize Final Report
            final_report = await strategic_synthesis_agent(financial_data, market_analysis, valuation_models)
            
            logging.info("--- Orchestrator: Workflow Completed Successfully ---")
            return final_report

    return "Orchestrator: Failed to complete the workflow."

def run_equity_research(ticker: str) -> str:
    try:
        return asyncio.run(run_equity_research_async(ticker))
    except Exception as e:
        logging.error(f"Failed to execute the asyncio event loop: {e}", exc_info=True)
        return f"A critical application error occurred: {e}"