import streamlit as st
import json
import os
from dotenv import load_dotenv
from google import genai  # <-- Using the modern SDK

# Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# --- UI CONFIGURATION ---
st.set_page_config(page_title="NetGuard AI", page_icon="🛡️", layout="centered")

st.title("🛡️ NetGuard AI: Incident Summarizer")
st.markdown("Transforms raw technical data (firewall logs, PCAP summaries, or Windows event logs) into structured cybersecurity incident reports.")
st.markdown("---")

# --- INPUT SECTION ---
st.markdown("**Raw Telemetry**")
raw_logs = st.text_area(
    label="Raw Telemetry input",
    label_visibility="collapsed", 
    placeholder="Paste firewall logs, Windows Event Logs, PCAP summaries, or raw telemetry here...",
    height=250
)

# --- GENERATE BUTTON ---
if st.button("Generate Report", type="primary"):
    if not raw_logs.strip():
        st.warning("Please paste some telemetry data first.")
    elif not API_KEY:
        st.error("GEMINI_API_KEY not found. Please check your .env file.")
    else:
        with st.spinner("Analyzing threat telemetry..."):
            try:
                # 1. Initialize the modern Gemini client
                client = genai.Client(api_key=API_KEY)
                
                # 2. The Prompt
                prompt = f"""
                You are an expert Cybersecurity Incident Responder. Analyze the following raw telemetry data 
                and generate a structured incident report. 
                
                CRITICAL REQUIREMENTS:
                Please format your response cleanly and ensure it includes the following specific sections:
                1. Executive Summary
                2. Severity Score: Provide a rating from 1 to 10, followed by a brief justification for why this score was chosen based on business risk.
                3. Technical Findings: Identification of specific patterns (e.g., Brute Force, TKIP weaknessess or port scanning
                4. Remediation Steps: A clear, actionable steps for the IT team to take immediately.
                
                Raw Telemetry:
                {raw_logs}
                """

                # 3. Call the API using the 1.5 free tier model and new syntax
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                report_text = response.text
                
                # --- RESULTS DISPLAY ---
                st.success("Analysis Complete")
                st.markdown("### 📋 Executive Incident Report")
                st.markdown(report_text)
                
                # --- DOWNLOAD BUTTONS ---
                st.markdown("---")
                st.markdown("**Export Report:**")
                
                # Create the JSON format
                json_export = json.dumps({
                    "incident_summary": report_text,
                    "raw_telemetry_analyzed": raw_logs
                }, indent=4)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📄 Download as TXT",
                        data=report_text,
                        file_name="NetGuard_Report.txt",
                        mime="text/plain"
                    )
                    
                with col2:
                    st.download_button(
                        label="🧩 Download as JSON",
                        data=json_export,
                        file_name="NetGuard_Report.json",
                        mime="application/json"
                    )

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")