# 📈 AI Equity Research Analyst

A sophisticated equity research tool that leverages AI to provide comprehensive fundamental analysis of stocks. Built with Streamlit, Autogen, and FastMCP, this application fetches real-time financial data and generates professional investment analysis reports.

## ✨ Features

- **Real-time Financial Data**: Fetches live stock data using Yahoo Finance
- **AI-Powered Analysis**: Uses Google Gemini 2.0 Flash to generate comprehensive fundamental analysis
- **Professional Reports**: Structured analysis covering business summary, valuation metrics, and investment outlook
- **Interactive UI**: Clean, professional Streamlit interface with download functionality
- **MCP Integration**: Uses Model Context Protocol for robust tool orchestration
- **Global Stock Support**: Supports US stocks (AAPL) and international markets (TCS.NS for Indian stocks)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Autogen       │    │   FastMCP       │
│   Frontend      │───▶│   Orchestrator  │───▶│   Tool Server   │
│   (app.py)      │    │   (main.py)     │    │   (server.py)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                        ┌─────────────────┐    ┌─────────────────┐
                        │   Google Gemini │    │   Yahoo Finance │
                        │   2.0 Flash     │    │   Data API      │
                        └─────────────────┘    └─────────────────┘
```

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

# Install additional dependencies
pip install tiktoken
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Windows
echo GEMINI_API_KEY=your_gemini_api_key_here > .env

# macOS/Linux
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

Or manually create `.env` file with:
```
GEMINI_API_KEY=your-actual-gemini-api-key-here
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
3. **Click "🔍 Analyze Stock"**
4. **Wait for analysis** (typically 30-60 seconds)
5. **Review the report** with comprehensive fundamental analysis
6. **Download the report** as a Markdown file using the download button

## 📊 Sample Analysis Output

The tool generates structured reports including:

- **Business Summary**: Company description and operations
- **Key Metrics Table**: Market cap, P/E ratios, dividend yield, etc.
- **Valuation Analysis**: Commentary on pricing metrics
- **Profitability Assessment**: Dividend and return analysis
- **52-Week Range**: Stock price performance
- **Investment Conclusion**: Neutral summary and outlook

## 🛠️ Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Install missing dependencies
pip install tiktoken autogen-ext autogen-agentchat autogen-core
```

**2. API Key Errors**
- Verify your `.env` file exists and contains the correct API key
- Ensure your Google AI Studio account has available credits
- Check that the API key starts with `sk-`

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
python -m server

# Test stock data
python -c "import yfinance as yf; print('✅ yfinance OK')"
```

## 🔧 Advanced Configuration

### Custom Models

Edit `main.py` to change the AI model:
```python
model_client = GeminiChatCompletionClient(
    model="gemini-2.0-flash",
    api_key=gemini_api_key,
)
```

### Analysis Template

Modify the `system_message` in `main.py` to customize the analysis format and focus areas.

### UI Customization

Edit `app.py` to modify:
- Colors and styling
- Layout and components
- Additional input fields
- Export formats

## 📁 Project Structure

```
equity_research_analyst/
├── app.py              # Streamlit frontend
├── main.py             # Autogen orchestration
├── server.py           # FastMCP tool server
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .gitignore         # Git ignore rules
├── README.md          # This file
├── activate.sh        # Quick activation script
└── equity/            # Virtual environment (not in git)
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your Gemini API key secure and private
- Monitor your Gemini usage and costs
- The `.gitignore` file protects sensitive files automatically

## 📈 Supported Markets

- **US Markets**: NYSE, NASDAQ (e.g., AAPL, GOOGL)
- **Indian Markets**: NSE, BSE (add `.NS` or `.BO` suffix)
- **European Markets**: Various (add country suffix like `.L`, `.PA`)
- **Asian Markets**: Various (add country suffix like `.T` for Tokyo)

## 💰 Cost Considerations

- Uses Google Gemini 2.0 Flash (cost-effective model)
- Typical analysis costs ~$0.01-0.05 per request
- Monitor usage at [Google AI Studio](https://aistudio.google.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It does not constitute financial advice. Always consult with qualified financial professionals before making investment decisions.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Verify your environment setup
3. Check Gemini API status and credits
4. Review the project's issue tracker

## 🎯 Roadmap

- [ ] Support for more financial metrics
- [ ] Historical analysis capabilities
- [ ] Portfolio analysis features
- [ ] Multiple AI model support
- [ ] Real-time alerts and monitoring
- [ ] Advanced charting and visualization

---

**Happy Investing! 📈**
