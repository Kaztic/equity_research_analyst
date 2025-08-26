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
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton>button {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="color: #1f77b4; margin-bottom: 0.5rem;">Multi-Agent AI Equity Research Platform</h1>
    <p style="color: #666; font-size: 1.1rem;"> Analysis by a team of specialized AI agents</p>
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
        with st.spinner("Orchestrator is coordinating the AI agent team... This may take a moment."):
            try:
                # Call the main orchestrator function
                analysis_report = run_equity_research(ticker.strip().upper())
                
                if analysis_report:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.container():
                        st.markdown('<div class="report-container">', unsafe_allow_html=True)
                        st.markdown(analysis_report)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 Download Full Report",
                        data=analysis_report,
                        file_name=f"{ticker.strip().upper()}_comprehensive_analysis.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                else:
                    st.error("The agent team failed to generate an analysis. Please check the ticker and try again.")
            except Exception as e:
                st.error(f"A critical error occurred: {e}")
                st.info("Please ensure your GOOGLE_API_KEY is correctly configured in your .env file.")

# --- Footer ---
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0 1rem 0; margin-top: 3rem; border-top: 1px solid #ddd;">
    <p>Powered by Google Gemini & a Multi-Agent System Architecture</p>
    <p style="font-size: 0.8rem;">This is a technology demonstration and is not financial advice.</p>
</div>
""", unsafe_allow_html=True)