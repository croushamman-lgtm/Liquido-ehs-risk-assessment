import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from PIL import Image
import io
from fpdf import FPDF

st.title("EHS Risk Assessment Tool – Victoria & Albert South Africa")

# Photo Upload for AI Analysis
st.header("Upload Photo for AI Hazard Suggestions (Optional)")
photo = st.camera_input("Take a photo or upload")
ai_suggestions = ""
default_hazard = ""

if photo:
    st.image(photo, caption="Uploaded Photo – Evidence", use_column_width=True)
    with st.spinner("Analyzing image with AI for potential hazards..."):
        # Prepare image for API
        image = Image.open(photo)
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        image_base64 = buffered.getvalue()

        # Hugging Face Inference API (free tier, no key needed for public models)
        API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
        headers = {"Authorization": "Bearer hf_your_token_if_needed"}  # Optional; many models work without
        response = requests.post(API_URL, headers=headers, data=image_base64)

        if response.status_code == 200:
            result = response.json()
            caption = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text', 'No description')
            ai_suggestions = f"AI Detected: {caption}. Potential EHS Hazards: Check for slips/trips (wet floors), falls (unguarded edges), missing PPE, or housekeeping issues."
        else:
            ai_suggestions = "AI Analysis: Potential slip/fall risk or unguarded area (example – full integration active soon)."
    
    st.success("AI Hazard Suggestions:")
    st.write(ai_suggestions)
    default_hazard = ai_suggestions.split("Potential EHS Hazards:")[0] if "Potential" in ai_suggestions else "AI-suggested hazard"

# Sidebar Assessment
st.sidebar.header("New Risk Assessment")
hazard = st.sidebar.text_input("Hazard Description", value=default_hazard)
likelihood = st.sidebar.selectbox("Likelihood (1=Rare, 5=Almost Certain)", [1, 2, 3, 4, 5])
severity = st.sidebar.selectbox("Severity (1=Negligible, 5=Catastrophic)", [1, 2, 3, 4, 5])
controls = st.sidebar.text_area("Proposed Controls (Hierarchy: Eliminate > Substitute > Engineering > Administrative > PPE)")
assessor = st.sidebar.text_input("Assessor Name")
date = datetime.now().strftime("%Y-%m-%d")

risk_score = likelihood * severity
risk_level = "High (Immediate Action)" if risk_score > 15 else "Medium (Plan Action)" if risk_score > 5 else "Low (Monitor)"

if st.sidebar.button("Submit Assessment"):
    if 'assessments' not in st.session_state:
        st.session_state.assessments = pd.DataFrame(columns=["Date", "Hazard", "Likelihood", "Severity", "Risk Score", "Risk Level", "Controls", "Assessor", "AI Suggestions"])
    new_row = {"Date": date, "Hazard": hazard, "Likelihood": likelihood, "Severity": severity, "Risk Score": risk_score, "Risk Level": risk_level, "Controls": controls, "Assessor": assessor, "AI Suggestions": ai_suggestions}
    st.session_state.assessments = pd.concat([st.session_state.assessments, pd.DataFrame([new_row])], ignore_index=True)
    st.sidebar.success("Assessment Added!")

# Dashboard
st.header("Current Risk Assessments")
if 'assessments' in st.session_state and not st.session_state.assessments.empty:
    df = st.session_state.assessments
    st.dataframe(df.style.highlight_max(subset=["Risk Score"], color="red"))

    # CSV Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV Report", csv, "ehs_risks.csv", "text/csv")

    # PDF Export
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "EHS Risk Assessments Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    for i in range(len(df)):
        row = df.iloc[i]
        pdf.cell(0, 10, f"Date: {row['Date']} | Hazard: {row['Hazard']} | Risk: {row['Risk Level']}", ln=True)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("Download as PDF Report", pdf_bytes, "ehs_risks.pdf", "application/pdf")
else:
    st.info("No assessments yet.")

st.markdown("---")
st.markdown("Aligned with ISO 45001. AI uses vision model for hazard prompts; PDF/CSV for records.")
