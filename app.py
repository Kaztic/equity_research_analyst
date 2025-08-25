# app.py

import streamlit as st
from main import run_equity_research

st.set_page_config(
    page_title="Multi-Agent AI Equity Research", 
    page_icon="🤖",
    layout="wide"
)

# --- UI Styling ---
st.markdown("""
<style>
    .report-container {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton>button {
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.75rem 1.5rem;
    }
    h1, h2, h3 {
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="color: #1f77b4; margin-bottom: 0.5rem;">Multi-Agent AI Equity Research Platform</h1>
    <p style="color: #666; font-size: 1.1rem;">Comprehensive analysis by a team of specialized AI agents</p>
</div>
""", unsafe_allow_html=True)

# --- Input Section ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ticker = st.text_input(
        "Enter a stock ticker to begin the analysis:", 
        placeholder="e.g., GOOGL, MSFT, AAPL"
    )
    
    analyze_button = st.button(
        "🚀 Run Analysis", 
        type="primary",
        use_container_width=False
    )

# --- Analysis Section ---
if analyze_button:
    if not ticker.strip():
        st.warning("Please enter a valid stock ticker.")
    else:
        with st.spinner("Executing multi-agent workflow... Running financial models and market analysis (this can take up to 60 seconds)."):
            try:
                analysis_report = run_equity_research(ticker.strip().upper())
                
                if analysis_report:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    with st.container():
                        st.markdown('<div class="report-container">', unsafe_allow_html=True)
                        st.markdown(analysis_report)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        label="Download Full Report (.md)",
                        data=analysis_report,
                        file_name=f"{ticker.strip().upper()}_SOTA_Analysis.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                else:
                    st.error("The agent team failed to generate a report. Please check the ticker and logs.")
            except Exception as e:
                st.error(f"A critical system error occurred: {e}")
                st.info("Check your console logs and ensure your GOOGLE_API_KEY is correctly configured.")

# --- Footer ---
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0 1rem 0; margin-top: 3rem; border-top: 1px solid #ddd;">
    <p>Powered by Google Gemini & a Multi-Agent System Architecture</p>
    <p style="font-size: 0.8rem;">This is a technology demonstration and is not financial advice.</p>
</div>
""", unsafe_allow_html=True)