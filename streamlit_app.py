import streamlit as st
import pandas as pd
from datetime import datetime

# App Title
st.title("EHS Risk Assessment Tool – Victoria & Albert South Africa")

# Sidebar for User Input
st.sidebar.header("New Risk Assessment")
hazard = st.sidebar.text_input("Hazard Description")
likelihood = st.sidebar.selectbox("Likelihood (1= Rare, 5= Almost Certain)", [1, 2, 3, 4, 5])
severity = st.sidebar.selectbox("Severity (1= Negligible, 5= Catastrophic)", [1, 2, 3, 4, 5])
controls = st.sidebar.text_area("Proposed Controls (Apply Hierarchy: Eliminate > Substitute > Engineering > Administrative > PPE)")
assessor = st.sidebar.text_input("Assessor Name")
date = datetime.now().strftime("%Y-%m-%d")

# Calculate Risk Score
risk_score = likelihood * severity
risk_level = "High (Immediate Action)" if risk_score > 15 else "Medium (Plan Action)" if risk_score > 5 else "Low (Monitor)"

# Button to Add Assessment
if st.sidebar.button("Submit Assessment"):
    if 'assessments' not in st.session_state:
        st.session_state.assessments = pd.DataFrame(columns=["Date", "Hazard", "Likelihood", "Severity", "Risk Score", "Risk Level", "Controls", "Assessor"])
    new_row = {"Date": date, "Hazard": hazard, "Likelihood": likelihood, "Severity": severity, "Risk Score": risk_score, "Risk Level": risk_level, "Controls": controls, "Assessor": assessor}
    st.session_state.assessments = pd.concat([st.session_state.assessments, pd.DataFrame([new_row])], ignore_index=True)
    st.sidebar.success("Assessment Added!")

# Display Assessments Table
st.header("Current Risk Assessments")
if 'assessments' in st.session_state and not st.session_state.assessments.empty:
    st.dataframe(st.session_state.assessments.style.highlight_max(subset=["Risk Score"], color="red"))
    # Export to CSV
    csv = st.session_state.assessments.to_csv(index=False).encode('utf-8')
    st.download_button("Download Assessments as CSV Report", csv, "ehs_risks.csv", "text/csv")
else:
    st.info("No assessments recorded yet. Add one using the sidebar.")

# Footer
st.markdown("---")
st.markdown("Aligned with ISO 45001 Clause 6.1 (Risks & Opportunities) and NEBOSH risk assessment principles. For site-specific customization, provide details.")
