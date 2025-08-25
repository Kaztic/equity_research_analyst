# server.py

import json
from mcp.server.fastmcp import FastMCP
import yfinance as yf
from googlesearch import search

# Initialize the MCP server
mcp = FastMCP("EnhancedFinanceTools")

@mcp.tool()
def get_stock_fundamentals(ticker: str) -> dict:
    """Fetches key fundamental financial data for a given stock ticker from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
        
        # Select key-value pairs that are JSON serializable
        data = {
            "ticker": ticker,
            "companyName": info.get("shortName"),
            "longBusinessSummary": info.get("longBusinessSummary"),
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "priceToBook": info.get("priceToBook"),
            "dividendYield": info.get("dividendYield"),
            "payoutRatio": info.get("payoutRatio"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "averageVolume": info.get("averageVolume"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "fullTimeEmployees": info.get("fullTimeEmployees"),
            "returnOnEquity": info.get("returnOnEquity"),
            "debtToEquity": info.get("debtToEquity"),
            "totalRevenue": info.get("totalRevenue"),
            "netIncomeToCommon": info.get("netIncomeToCommon"),
            "trailingEps": info.get("trailingEps"),
            "earningsGrowth": info.get("earningsGrowth"),
            "revenueGrowth": info.get("revenueGrowth"),
            "heldPercentInstitutions": info.get("heldPercentInstitutions")
        }
        # Filter out any None values to ensure clean data
        return {k: v for k, v in data.items() if v is not None}

    except Exception as e:
        print(f"Error fetching fundamentals for {ticker}: {e}")
        return {"error": f"Could not fetch fundamental data for {ticker}."}

@mcp.tool()
def get_historical_financials(ticker: str) -> dict:
    """Fetches the last 3 years of revenue and net income for trend analysis."""
    try:
        stock = yf.Ticker(ticker)
        # Fetch annual financial data
        financials = stock.financials
        
        if financials.empty:
            return {"error": "Could not retrieve financial statements."}

        # Extract the last 3 years of Total Revenue and Net Income
        report = {}
        years = financials.columns[:3] # Get the most recent 3 years
        
        for year in years:
            year_str = str(year.year)
            report[year_str] = {
                "totalRevenue": financials.loc['Total Revenue', year],
                "netIncome": financials.loc['Net Income', year]
            }
        
        return report

    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return {"error": "Failed to process historical financial data."}

@mcp.tool()
def perform_google_search(query: str, num_results: int = 5) -> str:
    """
    Performs a Google search for a given query and returns the top results as a single string.
    Useful for gathering qualitative data like news, industry trends, and competitor analysis.
    """
    try:
        print(f"Performing search for: {query}")
        # Using the 'googlesearch-python' library
        search_results = search(query, num_results=num_results, sleep_interval=1)
        
        output = ""
        for i, result in enumerate(search_results):
            output += f"Result {i+1}: {result}\n"
        
        # In a real-world scenario, you might want to visit these URLs and scrape content.
        # For this demo, returning the URLs and their titles is sufficient for the LLM.
        return output if output else "No search results found."

    except Exception as e:
        print(f"Error during Google search: {e}")
        return f"An error occurred during search: {e}"


if __name__ == "__main__":
    print("Starting Enhanced MCP server...")
    mcp.run(transport="stdio")