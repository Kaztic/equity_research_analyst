import asyncio
import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Configure logging for GroupChat visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
    ]
)

# Set up logger for our application
logger = logging.getLogger("EquityResearch")
logger.setLevel(logging.INFO)

# Also enable autogen logging
autogen_logger = logging.getLogger("autogen")
autogen_logger.setLevel(logging.INFO)

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
    from autogen_agentchat.teams import RoundRobinGroupChat  # type: ignore
except Exception:
    AssistantAgent = None  # type: ignore
    RoundRobinGroupChat = None  # type: ignore

try:
    from autogen_core import CancellationToken  # type: ignore
except Exception:
    CancellationToken = None  # type: ignore


load_dotenv()


async def _run_equity_research_async(ticker: str) -> str:
    logger.info(f"🚀 Starting multi-agent equity research for: {ticker}")
    
    if OpenAIChatCompletionClient is None or StdioServerParams is None or mcp_server_tools is None or AssistantAgent is None or RoundRobinGroupChat is None:
        raise ImportError(
            "Autogen packages not available. Please install/upgrade: "
            "pip install -U autogen-ext autogen-agentchat autogen-core openai"
        )
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    logger.info("🔧 Setting up MCP tools and model client...")
    stdio_params = StdioServerParams(command="python", args=["-m", "server"])
    tools = await mcp_server_tools(stdio_params)
    logger.info(f"✅ MCP tools ready: {len(tools)} tool(s) available")

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=openai_api_key,
    )

    logger.info("👥 Creating specialized agents...")
    
    # Agent 1: Financial Data Analyst - Fetches and analyzes raw financial data
    logger.info("📊 Setting up DataAnalyst agent...")
    data_analyst = AssistantAgent(
        name="DataAnalyst",
        model_client=model_client,
        tools=tools,
        reflect_on_tool_use=True,
        system_message=(
            "You are a Financial Data Analyst. Your role is to:\n"
            "1. FIRST, call get_stock_fundamentals tool to fetch financial data for the requested ticker\n"
            "2. Extract and summarize key financial metrics (P/E, P/B, market cap, dividend yield, etc.)\n"
            "3. Identify any data quality issues or missing values\n"
            "4. Present clean, organized financial data to other agents\n"
            "5. Only use factual data from the tool - no external knowledge\n\n"
            "Keep your response focused on data presentation and basic calculations."
        ),
    )

    # Agent 2: Market Research Analyst - Provides context and industry insights
    logger.info("🔍 Setting up MarketAnalyst agent...")
    market_analyst = AssistantAgent(
        name="MarketAnalyst", 
        model_client=model_client,
        system_message=(
            "You are a Market Research Analyst. Your role is to:\n"
            "1. Analyze the financial data provided by the DataAnalyst\n"
            "2. Provide context on valuation metrics (what do P/E, P/B ratios mean?)\n"
            "3. Comment on the company's financial health and profitability\n"
            "4. Assess the 52-week price range and what it indicates\n"
            "5. Identify potential strengths and risks based on the metrics\n\n"
            "Focus on interpreting the numbers and providing analytical insights."
        ),
    )

    # Agent 3: Report Writer - Synthesizes everything into a final report
    logger.info("📝 Setting up ReportWriter agent...")
    report_writer = AssistantAgent(
        name="ReportWriter",
        model_client=model_client,
        system_message=(
            "You are a Report Writer. Your role is to:\n"
            "1. Synthesize inputs from DataAnalyst and MarketAnalyst\n"
            "2. Create a professional, structured equity research report\n"
            "3. Use the EXACT Markdown template below:\n\n"
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
            "- [Analysis of P/E and P/B ratios]\n\n"
            "### Profitability & Shareholder Return\n"
            "- [Analysis of dividend yield and profitability]\n\n"
            "### 52-Week Range\n"
            "- {fiftyTwoWeekLow_formatted} — {fiftyTwoWeekHigh_formatted}\n\n"
            "### Conclusion\n"
            "[2-3 sentence neutral summary]\n\n"
            "Format numbers with thousands separators. Show percentages with % sign. If data missing, use 'N/A'."
        ),
    )

    # Create GroupChat with the three agents
    logger.info("🤝 Creating GroupChat with RoundRobin orchestration...")
    group_chat = RoundRobinGroupChat([data_analyst, market_analyst, report_writer])
    logger.info(f"✅ GroupChat ready with {len([data_analyst, market_analyst, report_writer])} agents")

    prompt = (
        f"Team, please collaborate to provide a comprehensive fundamental analysis for {ticker}. "
        f"DataAnalyst: Start by fetching financial data. "
        f"MarketAnalyst: Then analyze the metrics and provide insights. "
        f"ReportWriter: Finally, create a structured report. "
        f"Work together through multiple rounds if needed to ensure quality."
    )

    # Run the group chat conversation
    logger.info("🚀 Starting GroupChat conversation...")
    logger.info("=" * 80)
    logger.info(f"📋 TASK: {prompt}")
    logger.info("=" * 80)
    
    try:
        # Simple run without termination condition - will use default turn limits
        result = await group_chat.run(task=prompt)
        logger.info("✅ GroupChat conversation completed successfully!")
    except Exception as e:
        logger.error(f"❌ GroupChat error: {str(e)}")
        return f"Error during multi-agent analysis: {str(e)}"

    # Extract clean text content from the GroupChat result
    logger.info("🔍 Extracting final analysis from GroupChat messages...")
    text: Optional[str] = None
    
    # Handle GroupChat results - look for the final report from ReportWriter
    if hasattr(result, 'messages') and result.messages:
        logger.info(f"📝 Found {len(result.messages)} messages in GroupChat result")
        
        # Log all messages for debugging
        for i, message in enumerate(result.messages):
            if hasattr(message, 'source'):
                logger.info(f"💬 Message {i+1}: {message.source}")
            elif hasattr(message, 'content'):
                logger.info(f"💬 Message {i+1}: {str(message.content)[:100]}...")
        
        # Look through messages in reverse order to find the final report
        for message in reversed(result.messages):
            if hasattr(message, 'source') and message.source == "ReportWriter":
                logger.info("🎯 Found ReportWriter message!")
                if hasattr(message, 'content') and isinstance(message.content, str):
                    content = message.content.strip()
                    if "## Fundamental Analysis:" in content:
                        text = content
                        logger.info("✅ Successfully extracted final report from ReportWriter")
                        break
            elif hasattr(message, 'content') and isinstance(message.content, str):
                content = message.content.strip()
                if "## Fundamental Analysis:" in content:
                    text = content
                    logger.info("✅ Found formatted analysis in message")
                    break
    
    # Fallback: look for any message with the analysis format
    if text is None and hasattr(result, 'messages') and result.messages:
        for message in reversed(result.messages):
            if hasattr(message, 'content') and isinstance(message.content, str):
                text = message.content.strip()
                break
    
    # Final fallback: convert to string and extract
    if text is None:
        result_str = str(result)
        if "## Fundamental Analysis:" in result_str:
            start_idx = result_str.find("## Fundamental Analysis:")
            if start_idx != -1:
                text = result_str[start_idx:].strip()
                # Clean up any trailing metadata
                lines = text.split('\n')
                clean_lines = []
                for line in lines:
                    if (line.strip().startswith("type=") or 
                        line.strip().startswith("TextMessage") or
                        line.strip().startswith("source=")):
                        break
                    clean_lines.append(line)
                text = '\n'.join(clean_lines).strip()
    
    if text is None or not text.strip():
        logger.warning("⚠️  No suitable analysis found in GroupChat messages")
        text = "Multi-agent analysis could not be generated. Please try again."
    else:
        logger.info(f"📄 Final analysis ready! Length: {len(text)} characters")

    logger.info("🏁 Multi-agent equity research completed!")
    logger.info("=" * 80)
    
    return text


def run_equity_research(ticker: str) -> str:
    logger.info(f"🎯 API CALL: run_equity_research('{ticker}')")
    try:
        result = asyncio.run(_run_equity_research_async(ticker))
        logger.info("🎉 API CALL COMPLETED SUCCESSFULLY")
        return result
    except Exception as e:
        logger.error(f"💥 API CALL FAILED: {str(e)}")
        return f"Analysis failed: {str(e)}"


if __name__ == "__main__":
    print(run_equity_research("AAPL"))