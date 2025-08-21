import asyncio
import os
from typing import Optional
from dotenv import load_dotenv

# Robust imports with fallbacks for different autogen versions
try:
    from autogen_ext.models.openai import OpenAIChatCompletionClient  # type: ignore
except Exception:
    try:
        # Some versions may expose a different path/name
        from autogen_ext.models.openai_chat import (  # type: ignore
            OpenAIChatCompletionClient,
        )
    except Exception:
        OpenAIChatCompletionClient = None  # type: ignore

try:
    from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools  # type: ignore
except Exception:
    try:
        # Newer versions may place these in mcp_client
        from autogen_ext.tools.mcp_client import (  # type: ignore
            StdioServerParams,
            mcp_server_tools,
        )
    except Exception:
        StdioServerParams = None  # type: ignore
        mcp_server_tools = None  # type: ignore

try:
    from autogen_agentchat.agents import AssistantAgent  # type: ignore
except Exception:
    AssistantAgent = None  # type: ignore

try:
    from autogen_core import CancellationToken  # type: ignore
except Exception:
    CancellationToken = None  # type: ignore


load_dotenv()


async def _run_equity_research_async(ticker: str) -> str:
    if OpenAIChatCompletionClient is None or StdioServerParams is None or mcp_server_tools is None or AssistantAgent is None:
        raise ImportError(
            "Autogen packages not available. Please install/upgrade: "
            "pip install -U autogen-ext autogen-agentchat autogen-core openai"
        )
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    stdio_params = StdioServerParams(command="python", args=["-m", "server"])
    tools = await mcp_server_tools(stdio_params)

    system_message = (
        "You are a helpful equity research analyst. When the user provides a stock ticker, you MUST first "
        "call the get_stock_fundamentals tool to fetch its financial data. Rely ONLY on the tool data; do not "
        "use outside knowledge. Return the final answer as clean Markdown using the EXACT template below.\n\n"
        "TEMPLATE (fill values; keep headings):\n"
        "## Fundamental Analysis: {companyName} ({ticker})\n\n"
        "### Business Summary\n"
        "{businessSummary}\n\n"
        "### Key Metrics\n"
        "| Metric | Value |\n|---|---|\n"
        "| Market Cap | {marketCap_formatted} |\n"
        "| Trailing P/E | {trailingPE_formatted} |\n"
        "| Forward P/E | {forwardPE_formatted} |\n"
        "| Price-to-Book | {priceToBook_formatted} |\n"
        "| Dividend Yield | {dividendYield_percent} |\n"
        "| 52-Week Low | {fiftyTwoWeekLow_formatted} |\n"
        "| 52-Week High | {fiftyTwoWeekHigh_formatted} |\n\n"
        "### Valuation\n"
        "- Comment on P/E levels (trailing vs. forward) using the numbers above.\n"
        "- Comment on P/B ratio.\n\n"
        "### Profitability & Shareholder Return\n"
        "- Comment on dividendYield.\n\n"
        "### 52-Week Range\n"
        "- {fiftyTwoWeekLow_formatted} — {fiftyTwoWeekHigh_formatted}\n\n"
        "### Conclusion\n"
        "Provide a brief, neutral summary (2-3 sentences).\n\n"
        "FORMATTING RULES: If a value is missing, show 'N/A'. Add thousands separators for large numbers. "
        "Show percentages with a % sign (e.g., 4.2%). Do not include any preamble or explanations—only the Markdown."
    )

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=openai_api_key,
    )

    analyst = AssistantAgent(
        name="analyst",
        model_client=model_client,
        tools=tools,
        reflect_on_tool_use=True,
        system_message=system_message,
    )

    prompt = f"Please provide a fundamental analysis for the stock: {ticker}"

    # Run the conversation and capture the assistant's final output
    try:
        if CancellationToken:
            result = await analyst.run(task=prompt, cancellation_token=CancellationToken())
        else:
            result = await analyst.run(task=prompt)
    except Exception as e:
        return f"Error during analysis: {str(e)}"

    # Extract clean text content from the result
    text: Optional[str] = None
    
    # Handle different result types
    if hasattr(result, 'messages') and result.messages:
        # Get the last message from the conversation
        last_message = result.messages[-1]
        if hasattr(last_message, 'content') and isinstance(last_message.content, str):
            text = last_message.content.strip()
    elif hasattr(result, 'content') and isinstance(result.content, str):
        text = result.content.strip()
    elif hasattr(result, 'text') and isinstance(result.text, str):
        text = result.text.strip()
    
    # Fallback: convert to string and try to extract clean content
    if text is None:
        result_str = str(result)
        # Try to extract markdown content if it's embedded in a larger structure
        if "## Fundamental Analysis:" in result_str:
            # Find the start of the markdown content
            start_idx = result_str.find("## Fundamental Analysis:")
            if start_idx != -1:
                # Extract from the markdown start to the end, cleaning up any trailing metadata
                text = result_str[start_idx:].strip()
                # Remove any trailing object representations or metadata
                lines = text.split('\n')
                clean_lines = []
                for line in lines:
                    # Stop at lines that look like object metadata
                    if line.strip().startswith("type=") or line.strip().startswith("TextMessage"):
                        break
                    clean_lines.append(line)
                text = '\n'.join(clean_lines).strip()
    
    if text is None or not text.strip():
        text = "Analysis could not be generated. Please try again."

    return text


def run_equity_research(ticker: str) -> str:
    try:
        return asyncio.run(_run_equity_research_async(ticker))
    except Exception as e:
        return f"Analysis failed: {str(e)}"


if __name__ == "__main__":
    print(run_equity_research("AAPL"))