# server.py

from mcp.server.fastmcp import FastMCP
import yfinance as yfinance

# Initialize the MCP server
mcp = FastMCP("FinanceTools")

@mcp.tool()
def get_stock_fundamentals(ticker: str) -> dict:
    """Fetches key fundamental financial data for a given stock ticker from Yahoo Finance."""
    try:
        stock = yfinance.Ticker(ticker)
        info = stock.info or {}
    except Exception:
        info = {}

    data = {
        "ticker": ticker,
        "companyName": info.get("shortName", "N/A"),
        "businessSummary": info.get("longBusinessSummary", "N/A"),
        "marketCap": info.get("marketCap", "N/A"),
        "trailingPE": info.get("trailingPE", "N/A"),
        "forwardPE": info.get("forwardPE", "N/A"),
        "priceToBook": info.get("priceToBook", "N/A"),
        "dividendYield": info.get("dividendYield", "N/A"),
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh", "N/A"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow", "N/A"),
    }

    return data

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport="stdio")