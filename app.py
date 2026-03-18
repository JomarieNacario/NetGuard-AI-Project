import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables and configure Gemini
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
  genai.configure(api_key=api_key)
else:
  st.error("GEMINI_API_KEY not found. Pleasr check your .env file.")

  # Page configuration
  st.set_page_config(page_title="NetGuard AI Prototype", layout="wide")
  st.time("🛡️ NetGuard AI: Log Analyzer")

  # Sidebar for controls
  with st.sidebar:
    st.header("Configuration")
    report_type = st.selectbox(
      "Select Report Audience",
      ["Executive Summary", "Technical Deep Dive", "Actionable Remediation"]
    )
# Main upload area
uploaded_file = st.file_uploader("Upload Security Log File", type=["txt", "csv","json"])
if uploaded_file is not None:
  st.success(f"File '{uploaded_file.name}' uploaded successfully!")
  # Placeholder for Phase 3: Log Processing
  st.info("Log processing logic will go here.")