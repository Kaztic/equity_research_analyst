# server.py

import json
import yfinance as yf
import pandas as pd
from mcp.server.fastmcp import FastMCP
from googlesearch import search
import numpy as np

# Initialize the MCP server
mcp = FastMCP("StateOfTheArtFinanceTools")

def convert_timestamps_to_strings(obj):
    """Recursively convert all pandas Timestamps and other non-serializable objects to strings."""
    import pandas as pd
    
    if isinstance(obj, dict):
        return {key: convert_timestamps_to_strings(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_timestamps_to_strings(item) for item in obj]
    elif isinstance(obj, (pd.Timestamp, pd.NaT.__class__)):
        return str(obj)
    elif hasattr(obj, 'isoformat'):  # datetime objects
        return obj.isoformat()
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    else:
        return obj

@mcp.tool()
def get_comprehensive_financial_data(ticker: str) -> dict:
    """Fetches a wide range of financial data and robustly sanitizes it for JSON."""
    try:
        stock = yf.Ticker(ticker)

        # Fetch all data structures from yfinance
        info = stock.info or {}
        
        # Safely get DataFrames with empty checks
        try:
            financials = stock.financials
            if financials is None or financials.empty:
                financials = {}
            else:
                financials = financials.to_dict()
        except:
            financials = {}
            
        try:
            balance_sheet = stock.balance_sheet
            if balance_sheet is None or balance_sheet.empty:
                balance_sheet = {}
            else:
                balance_sheet = balance_sheet.to_dict()
        except:
            balance_sheet = {}
            
        try:
            cashflow = stock.cashflow
            if cashflow is None or cashflow.empty:
                cashflow = {}
            else:
                cashflow = cashflow.to_dict()
        except:
            cashflow = {}
            
        try:
            major_holders = stock.major_holders
            if major_holders is None or major_holders.empty:
                major_holders = {}
            else:
                major_holders = major_holders.to_dict()
        except:
            major_holders = {}
            
        try:
            insider_transactions = stock.insider_transactions
            if insider_transactions is None or insider_transactions.empty:
                insider_transactions = []
            else:
                insider_transactions = insider_transactions.to_dict('records')
        except:
            insider_transactions = []

        # Create data structure
        data = {
            "info": info,
            "financials": financials,
            "balance_sheet": balance_sheet,
            "cashflow": cashflow,
            "major_holders": major_holders,
            "insider_transactions": insider_transactions,
        }

        # --- Robust Sanitization Step ---
        # Convert all timestamps and non-serializable objects
        sanitized_data = convert_timestamps_to_strings(data)
        
        # Select key info fields to avoid overwhelming the LLM context
        key_info = {
            "ticker": ticker, "shortName": sanitized_data["info"].get("shortName"),
            "longBusinessSummary": sanitized_data["info"].get("longBusinessSummary"), "sector": sanitized_data["info"].get("sector"),
            "industry": sanitized_data["info"].get("industry"), "marketCap": sanitized_data["info"].get("marketCap"),
            "enterpriseValue": sanitized_data["info"].get("enterpriseValue"), "trailingPE": sanitized_data["info"].get("trailingPE"),
            "forwardPE": sanitized_data["info"].get("forwardPE"), "pegRatio": sanitized_data["info"].get("pegRatio"),
            "priceToBook": sanitized_data["info"].get("priceToBook"), "enterpriseToEbitda": sanitized_data["info"].get("enterpriseToEbitda"),
            "returnOnEquity": sanitized_data["info"].get("returnOnEquity"), "debtToEquity": sanitized_data["info"].get("debtToEquity"),
            "revenueGrowth": sanitized_data["info"].get("revenueGrowth"), "earningsGrowth": sanitized_data["info"].get("earningsGrowth"),
            "heldPercentInstitutions": sanitized_data["info"].get("heldPercentInstitutions"), "sharesOutstanding": sanitized_data["info"].get("sharesOutstanding")
        }
        # Replace the original 'info' with our curated, cleaner version
        sanitized_data["info"] = {k: v for k, v in key_info.items() if v is not None}
        
        return sanitized_data

    except Exception as e:
        print(f"Error fetching comprehensive data for {ticker}: {e}")
        # Make sure to return the error in the expected format
        return {"error": f"Failed to fetch comprehensive data. The ticker might be invalid or there was a data processing error: {e}"}

@mcp.tool()
def perform_dcf_and_monte_carlo(financial_data: dict) -> dict:
    """
    Performs a Discounted Cash Flow (DCF) analysis and a Monte Carlo simulation.
    This is a simplified model for demonstration purposes.
    """
    try:
        cashflow_statement = financial_data.get("cashflow")
        info = financial_data.get("info")

        if not cashflow_statement or not info:
            return {"error": "Insufficient data for DCF calculation. Cashflow or Info missing."}

        # --- DCF Calculation ---
        # The cashflow data structure has timestamps as keys and metrics as sub-keys
        # Get the latest year's data
        if not cashflow_statement:
            return {"error": "No cashflow data available."}
            
        latest_year = max(cashflow_statement.keys())
        latest_data = cashflow_statement[latest_year]
        
        # Try to get Free Cash Flow directly first
        fcf = latest_data.get('Free Cash Flow')
        
        if fcf is None:
            # Try to calculate FCF from Operating Cash Flow and Capex
            op_cash = (
                latest_data.get('Operating Cash Flow') or
                latest_data.get('Total Cash From Operating Activities') or
                latest_data.get('Net Cash From Operating Activities') or
                latest_data.get('Cash From Operating Activities')
            )
            
            capex = (
                latest_data.get('Capital Expenditure') or
                latest_data.get('Capital Expenditures') or
                latest_data.get('Capex') or
                latest_data.get('Net PPE Purchase And Sale')
            )
            
            if op_cash is not None and capex is not None:
                fcf = op_cash + capex  # Capex is usually negative
            else:
                available_fields = list(latest_data.keys())[:10]
                return {"error": f"Could not find required cashflow fields. Available fields include: {available_fields}"}
        
        if fcf is None or fcf == 0:
            return {"error": "Free Cash Flow is zero or unavailable for DCF calculation."}

        # Assumptions
        discount_rate_mean = 0.09
        growth_rate_mean = info.get("revenueGrowth", 0.05) or 0.05
        terminal_growth_rate = 0.025
        projection_years = 5
        
        future_fcf = [fcf * (1 + growth_rate_mean)**i for i in range(1, projection_years + 1)]
        terminal_value = (future_fcf[-1] * (1 + terminal_growth_rate)) / (discount_rate_mean - terminal_growth_rate)
        present_values = [fcf / (1 + discount_rate_mean)**i for i, fcf in enumerate(future_fcf, 1)]
        present_terminal_value = terminal_value / (1 + discount_rate_mean)**projection_years
        enterprise_value = sum(present_values) + present_terminal_value
        
        shares_outstanding = info.get("sharesOutstanding")
        if not shares_outstanding:
            return {"error": "Shares outstanding not available."}
            
        dcf_intrinsic_value = enterprise_value / shares_outstanding

        # --- Monte Carlo Simulation ---
        simulations = 1000
        results = []
        for _ in range(simulations):
            sim_growth_rate = np.random.normal(growth_rate_mean, 0.02)
            sim_discount_rate = np.random.normal(discount_rate_mean, 0.015)
            
            if sim_discount_rate <= terminal_growth_rate: continue

            sim_future_fcf = [fcf * (1 + sim_growth_rate)**i for i in range(1, projection_years + 1)]
            sim_terminal_value = (sim_future_fcf[-1] * (1 + terminal_growth_rate)) / (sim_discount_rate - terminal_growth_rate)
            sim_pv = [fcf / (1 + sim_discount_rate)**i for i, fcf in enumerate(sim_future_fcf, 1)]
            sim_pv_terminal = sim_terminal_value / (1 + sim_discount_rate)**projection_years
            sim_ev = sum(sim_pv) + sim_pv_terminal
            sim_intrinsic_value = sim_ev / shares_outstanding
            results.append(sim_intrinsic_value)
        
        if not results:
             return {"error": "Monte Carlo simulation failed to produce valid results."}

        return {
            "dcf_base_value": dcf_intrinsic_value,
            "monte_carlo_median": np.median(results),
            "monte_carlo_range_25_75": [np.percentile(results, 25), np.percentile(results, 75)],
            "assumptions": {
                "discount_rate": discount_rate_mean,
                "short_term_growth_rate": growth_rate_mean,
                "terminal_growth_rate": terminal_growth_rate
            }
        }

    except Exception as e:
        print(f"Error in DCF/Monte Carlo: {e}")
        return {"error": f"An error occurred during financial modeling: {e}"}

@mcp.tool()
def perform_google_search(query: str, num_results: int = 7) -> str:
    """Performs a Google search to gather qualitative data like news and industry trends."""
    try:
        search_results = list(search(query, num_results=num_results, sleep_interval=1))
        return "\n".join(search_results) or "No results found."
    except Exception as e:
        return f"An error occurred during search: {e}"

if __name__ == "__main__":
    print("Starting State-of-the-Art MCP server...")
    mcp.run(transport="stdio")