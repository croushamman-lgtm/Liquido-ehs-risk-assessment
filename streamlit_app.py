import streamlit as st
import pandas as pd
from datetime import datetime
# Optional: For basic AI suggestions (expand later)
# from some_vision_library import analyze_image  # Placeholder for future integration

st.title("EHS Risk Assessment Tool – Victoria & Albert South Africa")

# Photo Upload Section
st.header("Upload Photo for AI Hazard Suggestions (Optional)")
photo = st.camera_input("Take a photo (mobile) or upload from gallery")
if photo:
    st.image(photo, caption="Uploaded Photo – Evidence", use_column_width=True)
    # Placeholder for AI analysis (we'll enhance this next)
    with st.spinner("Analyzing image for potential hazards..."):
        # Future: Call AI model here
        ai_suggestions = "Example AI Output: Potential slip hazard detected (wet floor); unguarded platform edge."  # Mock for now
    st.success("AI Suggestions:")
    st.write(ai_suggestions)
    # Auto-fill hazard field with suggestion
    default_hazard = "Walking on platform – slip/ fall risk (AI detected wet surface/ unguarded edge)"

# Sidebar for Manual/New Assessment
st.sidebar.header("New Risk Assessment")
hazard = st.sidebar.text_input("Hazard Description", value=default_hazard if photo else "")
likelihood = st.sidebar.selectbox("Likelihood (1=Rare, 5=Almost Certain)", [1, 2, 3, 4, 5])
severity = st.sidebar.selectbox("Severity (1=Negligible, 5=Catastrophic)", [1, 2, 3, 4, 5])
controls = st.sidebar.text_area("Proposed Controls (Hierarchy: Eliminate > Substitute > Engineering > Administrative > PPE)")
assessor = st.sidebar.text_input("Assessor Name")
date = datetime.now().strftime("%Y-%m-%d")

# Risk Calculation
risk_score = likelihood * severity
risk_level = "High (Immediate Action)" if risk_score > 15 else "Medium (Plan Action)" if risk_score > 5 else "Low (Monitor)"

if st.sidebar.button("Submit Assessment"):
    if 'assessments' not in st.session_state:
        st.session_state.assessments = pd.DataFrame(columns=["Date", "Hazard", "Likelihood", "Severity", "Risk Score", "Risk Level", "Controls", "Assessor", "Photo Evidence"])
    # Attach photo evidence link (placeholder – actual file name)
    photo_evidence = photo.name if photo else "None"
    new_row = {"Date": date, "Hazard": hazard, "Likelihood": likelihood, "Severity": severity, "Risk Score": risk_score, "Risk Level": risk_level, "Controls": controls, "Assessor": assessor, "Photo Evidence": photo_evidence}
    st.session_state.assessments = pd.concat([st.session_state.assessments, pd.DataFrame([new_row])], ignore_index=True)
    st.sidebar.success("Assessment Added!")

# Dashboard
st.header("Current Risk Assessments")
if 'assessments' in st.session_state and not st.session_state.assessments.empty:
    st.dataframe(st.session_state.assessments.style.highlight_max(subset=["Risk Score"], color="red"))
    csv = st.session_state.assessments.to_csv(index=False).encode('utf-8')
    st.download_button("Download Assessments as CSV Report", csv, "ehs_risks.csv", "text/csv")
else:
    st.info("No assessments yet. Add one via sidebar (photo optional).")

st.markdown("---")
st.markdown("Aligned with ISO 45001 and NEBOSH principles. Photo evidence supports audit trails.")
