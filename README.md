# 📈 AI Equity Research Analyst

A sophisticated equity research tool that leverages AI to provide comprehensive fundamental analysis of stocks. Built with Streamlit, Google Gemini AI, and FastMCP, this application fetches real-time financial data and generates professional investment analysis reports through a multi-agent system.

## ✨ Features

- **Real-time Financial Data**: Fetches live stock data using Yahoo Finance
- **AI-Powered Analysis**: Uses Google Gemini AI to generate comprehensive fundamental analysis
- **Multi-Agent System**: Three specialized AI agents working together for comprehensive analysis
- **Professional Reports**: Structured analysis covering business summary, valuation metrics, and investment outlook
- **Interactive UI**: Clean, professional Streamlit interface with download functionality
- **MCP Integration**: Uses Model Context Protocol for robust tool orchestration
- **Global Stock Support**: Supports US stocks and international markets

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Multi-Agent   │    │   FastMCP       │
│   Frontend      │───▶│   Orchestrator  │───▶│   Tool Server   │
│   (app.py)      │    │   (main.py)     │    │   (server.py)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                        ┌─────────────────┐    ┌─────────────────┐
                        │   Google Gemini │    │   Yahoo Finance │
                        │   AI Models     │    │   Data API      │
                        └─────────────────┘    └─────────────────┘
```

### **Data Flow Architecture**

```
┌─────────────────┐
│   User Input    │
│   (Stock Ticker)│
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Streamlit UI   │
│   (app.py)      │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Multi-Agent     │
│ Orchestrator    │
│   (main.py)     │
└─────────┬───────┘
          │
          ├─────────────────┬─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Agent 1:      │ │   Agent 2:      │ │   Agent 3:      │
│ Data Fetcher    │ │Financial Analyst│ │Investment      │
│ (MCP Tools)     │ │(Google Gemini)  │ │Advisor         │
└─────────┬───────┘ └─────────┬───────┘ └─────────┬───────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Yahoo Finance   │ │ Financial Data  │ │ Analysis +      │
│ Data via MCP    │ │ Processing      │ │ Outlook         │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Final Report    │
                    │ (Markdown)      │
                    └─────────────────┘
```

### **Multi-Agent System Components**

1. **Data Fetching Agent**: Retrieves financial data using MCP tools
2. **Financial Analyst Agent**: Analyzes data and generates structured reports
3. **Investment Advisor Agent**: Provides investment outlook and disclaimers

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Windows, macOS, or Linux

## 🚀 Quick Start

### 1. Get Your Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign up or log in to your Google account
3. Navigate to [API Keys](https://aistudio.google.com/app/apikey)
4. Click "Create API Key"
5. Name your key (e.g., "Equity Research Tool")
6. Copy the generated key
7. **Important**: Save this key securely - you won't be able to see it again!

### 2. Clone or Download the Project

```bash
git clone <your-repository-url>
cd equity_research_analyst
```

Or download and extract the project files to a folder named `equity_research_analyst`.

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

Create a `.env` file in the project root:

```bash
# Windows
echo GOOGLE_API_KEY=your_google_api_key_here > .env

# macOS/Linux
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

Or manually create `.env` file with:
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

## 🔄 Workflow Process

### **Step 1: Data Collection**
- The Data Fetching Agent uses MCP tools to retrieve real-time financial data
- Fetches key metrics: market cap, P/E ratios, dividend yield, 52-week range
- Validates data quality and handles errors gracefully

### **Step 2: Financial Analysis**
- The Financial Analyst Agent processes the raw data
- Uses Google Gemini AI to generate structured analysis
- Covers company overview, key metrics, and valuation analysis

### **Step 3: Investment Outlook**
- The Investment Advisor Agent provides balanced summary
- Generates forward-looking statements and risk disclaimers
- Ensures compliance with financial advisory standards

### **Step 4: Report Generation**
- Combines all agent outputs into a comprehensive report
- Formats in clean Markdown for easy reading and downloading
- Provides professional presentation suitable for investment research

## 📊 Sample Analysis Output

The tool generates structured reports including:

- **Company Overview**: Company description and business summary
- **Key Financial Metrics Analysis**: Market cap, P/E ratios, dividend yield analysis
- **Stock Performance**: 52-week high/low analysis and price range commentary
- **Investment Summary & Outlook**: Balanced assessment and forward-looking statements
- **Disclaimer**: Standard financial advisory disclaimers

## 🛠️ Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Install missing dependencies
pip install -r requirements.txt
```

**2. API Key Errors**
- Verify your `.env` file exists and contains the correct API key
- Ensure your Google AI Studio account has available credits
- Check that the API key is properly formatted

**3. Virtual Environment Issues**
```bash
# Deactivate and recreate environment
deactivate
rm -rf equity  # or Remove-Item -Recurse -Force equity on Windows
python -m venv equity
# Re-activate and reinstall dependencies
```

**4. Port Already in Use**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

**5. Streamlit Cache Issues**
```bash
# Clear Streamlit cache
streamlit cache clear
```

### Verification Commands

Test individual components:

```bash
# Test Gemini connection
python -c "from main import run_equity_research; print('✅ Gemini connection OK')"

# Test MCP server
python server.py

# Test stock data
python -c "import yfinance as yf; print('✅ yfinance OK')"
```

##  Configuration

### Custom Models

Edit `main.py` to change the AI model:
```python
model = GenerativeModel(model_name="gemini-1.5-flash")
```
 templates in `main.py` to customize the analysis format and focus areas.

## 📁 Project Structure

```
equity_research_analyst/
├── app.py              # Streamlit frontend
├── main.py             # Multi-agent orchestration system
├── server.py           # FastMCP tool server
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .gitignore         # Git ignore rules
├── README.md          # This file
├── env_template.txt   # Environment variables template
├── activate.sh        # Quick activation script (Linux/Mac)
├── start.bat          # Quick start script (Windows)
└── equity/            # Virtual environment (not in git)
```
## 📈 Supported Markets

- **US Markets**: NYSE, NASDAQ (e.g., AAPL, GOOGL)
- **Indian Markets**: NSE, BSE (add `.NS` or `.BO` suffix)
- **European Markets**: Various (add country suffix like `.L`, `.PA`)
- **Asian Markets**: Various (add country suffix like `.T` for Tokyo)
