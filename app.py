# app.py

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
    <h1 style="color: #1f77b4; margin-bottom: 0.5rem;">AI Equity Research Analyst</h1>
    <p style="color: #666; font-size: 1.1rem;">Get comprehensive fundamental analysis powered by AI</p>
</div>
""", unsafe_allow_html=True)

# Input section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h5>Enter a stock ticker to begin</h5>", unsafe_allow_html=True)
    ticker = st.text_input(
        "Stock Ticker", 
        placeholder="e.g., GOOGL, MSFT, AAPL",
        label_visibility="collapsed"
    )
    
    analyze_button = st.button(
        "Analyze Stock", 
        type="primary",
        use_container_width=True
    )

# Analysis section
if analyze_button:
    if not ticker.strip():
        st.warning("Please enter a valid stock ticker.")
    else:
        with st.spinner("Fetching data and generating analysis..."):
            try:
                # Call the main orchestrator function
                analysis_report = run_equity_research(ticker.strip().upper())
                
                if analysis_report:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(analysis_report)
                    
                    # Add download button
                    st.download_button(
                        label="Download Analysis",
                        data=analysis_report,
                        file_name=f"{ticker.strip().upper()}_analysis.md",
                        mime="text/markdown",
                        use_container_width=False
                    )
                else:
                    st.error("The agent team failed to generate an analysis. Please try another ticker.")
            except Exception as e:
                st.error(f"A critical error occurred: {e}")
                st.info("Please ensure your GOOGLE_API_KEY is correctly configured in your .env file.")

# Footer
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0 1rem 0; margin-top: 3rem; border-top: 1px solid #ddd;">
    <p>Powered by Google Gemini & a Multi-Agent System • Financial Data via Yahoo Finance</p>
    <p style="font-size: 0.8rem;">This is a technology demonstration and not financial advice.</p>
</div>
""", unsafe_allow_html=True)