import streamlit as st
from main import run_equity_research


st.set_page_config(
    page_title="AI Equity Research Analyst", 
    page_icon="📈",
    layout="wide"
)

# Header with custom styling
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="color: #1f77b4; margin-bottom: 0.5rem;">📈 AI Equity Research Analyst</h1>
    <p style="color: #666; font-size: 1.1rem;">Get comprehensive fundamental analysis powered by AI</p>
</div>
""", unsafe_allow_html=True)

# Input section with better styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### Enter Stock Details")
    ticker = st.text_input(
        "Stock Ticker", 
        placeholder="e.g., AAPL, TCS.NS, INFY.NS",
        help="Enter the stock ticker symbol. For Indian stocks, use .NS suffix (e.g., TCS.NS)"
    )
    
    analyze_button = st.button(
        "🔍 Analyze Stock", 
        type="primary",
        use_container_width=True
    )

# Analysis section
if analyze_button:
    if not ticker.strip():
        st.warning("⚠️ Please enter a valid stock ticker.")
    else:
        with st.spinner("🔄 Fetching data and generating analysis..."):
            try:
                analysis = run_equity_research(ticker.strip().upper())
                if analysis and isinstance(analysis, str):
                    # Create a container for the analysis with custom styling
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display the analysis in a clean container
                    with st.container():
                        st.markdown("""
                        # <div style="background-color: #f8f9fa; padding: 2rem; border-radius: 10px; border-left: 4px solid #1f77b4; margin-bottom: 2rem;">
                        # """, unsafe_allow_html=True)
                        
                        st.markdown(analysis)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add download button for the analysis
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            label="📄 Download Analysis",
                            data=analysis,
                            file_name=f"{ticker.strip().upper()}_analysis.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                else:
                    st.error("❌ No analysis returned. Please try another ticker.")
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                st.info("💡 Make sure you have set your OPENAI_API_KEY environment variable.")

# Footer
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0 1rem 0; margin-top: 3rem;">
    <p>Powered by OpenAI GPT-4 • Financial data from Yahoo Finance via yfinance</p>
    <p style="font-size: 0.8rem;">⚠️ This is for educational purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
