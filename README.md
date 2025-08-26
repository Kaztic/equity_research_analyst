# 📈 AI Equity Research Analyst

An equity research tool powered by a team of specialized AI agents. Built with Streamlit, Google Gemini AI, and FastMCP, this application provides comprehensive fundamental analysis of stocks using real-time financial data.

## Features

- **Multi-Agent AI System**: Three specialized agents working together for comprehensive analysis
- **Real-time Financial Data**: Live stock data from Yahoo Finance API
- **Market Intelligence**: News and industry trend analysis via Google Search
- **Professional Reports**: Structured investment analysis with scorecards and insights
- **Interactive UI**: Clean Streamlit interface with downloadable reports
- **Global Stock Support**: US and international markets (NYSE, NASDAQ, NSE, etc.)

## 🤖 Multi-Agent Architecture

```
┌─────────────────┐
│   User Input    │
│ (Stock Ticker)  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Streamlit UI    │
│    (app.py)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Multi-Agent     │
│  Orchestrator   │
│   (main.py)     │
└─────┬───────────┘
      │
      ├─────────────────┬─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Agent 1   │ │   Agent 2   │ │   Agent 3   │
│Quantitative │ │ Qualitative │ │ Synthesis & │
│  Analyst    │ │  Analyst    │ │ Reporting   │
└─────┬───────┘ └─────┬───────┘ └─────┬───────┘
      │               │               │
      ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ MCP Server  │ │Google Gemini│ │Google Gemini│
│ (server.py) │ │ AI Model    │ │ AI Model    │
└─────┬───────┘ └─────────────┘ └─────────────┘
      │
      ├─────────────────┬─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│Yahoo Finance│ │Google Search│ │ Final Report│
│Financial Data│ │ News & Data │ │ (Markdown)  │
└─────────────┘ └─────────────┘ └─────────────┘
```

## 🔄 Workflow Process

```
User Input → Streamlit UI → Multi-Agent Orchestrator
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│   AGENT 1:      │          │   AGENT 2:      │          │   AGENT 3:      │
│ Quantitative    │          │ Qualitative     │          │ Synthesis &     │
│ Analyst         │          │ Analyst         │          │ Reporting       │
│                 │          │                 │          │                 │
│ Fetches:        │          │ Researches:     │          │ Creates:        │
│ • Stock data    │          │ • Latest news   │          │ • Final report  │
│ • Fundamentals  │          │ • Industry trends│         │ • Scorecard     │
│ • 3yr financials│          │ • Market sentiment│        │ • Investment    │
│                 │          │                 │          │   thesis        │
│ Data Sources:   │          │ Data Sources:   │          │                 │
│ • Yahoo Finance │          │ • Google Search │          │ Uses Gemini AI  │
│ • Via MCP Tools │          │ • Gemini AI     │          │ to synthesize   │
└─────────────────┘          └─────────────────┘          └─────────────────┘
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      ▼
                          ┌─────────────────────┐
                          │   FINAL OUTPUT:     │
                          │ Comprehensive       │
                          │ Investment Report   │
                          │ (Downloadable MD)   │
                          └─────────────────────┘
```

## 🎯 The Three AI Agents

### 1. **Quantitative Analyst Agent** (`quantitative_analyst_agent`)
- **Role**: Numbers specialist - fetches and processes all financial data
- **Data Sources**: Yahoo Finance via MCP tools
- **Output**: 
  - Fundamental metrics (P/E, ROE, debt ratios, market cap)
  - 3-year historical financials (revenue, net income trends)
  - Key valuation and performance indicators

### 2. **Qualitative Analyst Agent** (`qualitative_analyst_agent`) 
- **Role**: Market research specialist - analyzes sentiment and trends
- **Data Sources**: Google Search for news and industry analysis
- **AI Processing**: Uses Gemini AI to synthesize search results
- **Output**:
  - Market sentiment analysis (bullish/bearish/neutral)
  - Industry outlook and competitive landscape
  - Recent news and analyst rating insights

### 3. **Synthesis & Reporting Agent** (`synthesis_reporting_agent`)
- **Role**: Report writer - combines all data into final analysis
- **AI Processing**: Uses Gemini AI to create comprehensive reports
- **Output**:
  - Executive summary with key takeaways
  - At-a-glance scorecard (valuation, health, growth, sentiment)
  - Investment thesis with strengths and risks
  - Professional markdown report ready for download

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Windows, macOS, or Linux

## 🚀 Quick Start

### 1. Get Your Google Gemini API Key

Visit [Google AI Studio (MakerSuite)](https://makersuite.google.com/)

### 2. Clone or Download the Project

```bash
git clone <repository-url>
cd equity_research_analyst
```

### 3. Set Up Virtual Environment

#### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv equity

# Activate virtual environment
.\equity\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv equity

# Activate virtual environment
source equity/bin/activate
```

### 4. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root and add the Google API Key:
```
GOOGLE_API_KEY=your-actual-google-api-key-here
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will start and display:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://your-ip:8501
```

## 📖 How to Use

1. **Open your browser** and navigate to `http://localhost:8501`
2. **Enter a stock ticker** in the input field:
   - US stocks: `AAPL`, `MSFT`, `GOOGL`, `TSLA`
   - Indian stocks: `TCS.NS`, `INFY.NS`, `RELIANCE.NS`
   - Other international stocks: Use appropriate suffix (e.g., `.L` for London)
3. **Click "Analyze Stock"**
4. **Wait for analysis** (typically 30-60 seconds)
5. **Review the report** with comprehensive fundamental analysis
6. **Download the report** as a Markdown file using the download button

## 🔄 How It Works

1. **User Input**: Enter any stock ticker (e.g., AAPL, TSLA, GOOGL)
2. **Agent 1** fetches live financial data from Yahoo Finance
3. **Agent 2** researches market sentiment and industry trends via Google Search  
4. **Agent 3** combines everything into a professional investment report
5. **Output**: Comprehensive analysis with scorecard, insights, and download option

## 📊 Sample Analysis Output

Each report includes:

- **📊 At-a-Glance Scorecard**: Valuation, Financial Health, Growth, Market Sentiment
- **📝 Executive Summary**: Key takeaways and investment highlights  
- **🏢 Company & Industry Overview**: Business model and sector context
- **📈 Financial Performance & Health**: 3-year trends, profitability, debt analysis
- **💰 Valuation Analysis**: P/E ratios, P/B ratios explained in simple terms
- **🔍 Investment Thesis**: Bull case strengths vs bear case risks
- **⚠️ Disclaimer**: Standard financial advisory disclaimers

##  Configuration

### Custom Models

Edit `main.py` to change the AI model:
```python
model = GenerativeModel(model_name="gemini-2.0-flash")
```
 templates in `main.py` to customize the analysis format and focus areas.

## 📁 Project Structure

```
equity_research_analyst/
├── app.py              # 🖥️  Streamlit frontend UI
├── main.py             # 🤖 Multi-agent orchestrator (3 AI agents)
├── server.py           # 🔧 FastMCP tool server (Yahoo Finance + Google Search)
├── requirements.txt    # 📦 Python dependencies
├── .env               # 🔑 Environment variables (create this)
├── README.md          # 📖 This documentation
├── env_template.txt   # 📝 Environment template
├── activate.sh        # 🐧 Linux/Mac activation script
├── start.bat          # 🪟 Windows start script
└── equity/            # 📂 Virtual environment folder
```
## 📈 Supported Markets

- **US Markets**: NYSE, NASDAQ (e.g., AAPL, GOOGL)
- **Indian Markets**: NSE, BSE (add `.NS` or `.BO` suffix)
- **European Markets**: Various (add country suffix like `.L`, `.PA`)
- **Asian Markets**: Various (add country suffix like `.T` for Tokyo)
