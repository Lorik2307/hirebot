import streamlit as st
import PyPDF2
import io
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="HireBot 🤖", page_icon="🤖")
st.title("🤖 HireBot — AI Job Application Assistant")
st.write("Paste a job description and your resume. HireBot will score your match, find gaps, and write you a cover letter.")

col1, col2 = st.columns(2)

with col1:
    job_description = st.text_area("📋 Paste Job Description", height=300)

with col2:
    st.markdown("📄 **Your Resume**")
    resume_pdf = st.file_uploader("Upload Resume as PDF", type=["pdf"])
    resume = st.text_area("Or paste your resume here", height=220)
    
    if resume_pdf:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(resume_pdf.read()))
        resume = ""
        for page in pdf_reader.pages:
            resume += page.extract_text()
        st.success(f"✅ PDF loaded — {len(pdf_reader.pages)} pages")

if st.button("🚀 Analyze My Application") and job_description and resume:
    
    with st.spinner("Analyzing your match..."):
        score_prompt = f"""You are a hiring expert. Given this job description and resume, respond ONLY in this exact format:

SCORE: [number 0-100]
MATCHED_SKILLS: [comma separated list]
MISSING_SKILLS: [comma separated list]
VERDICT: [one sentence]

Job Description:
{job_description}

Resume:
{resume}"""

        score_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": score_prompt}]
        )
        analysis = score_response.choices[0].message.content

    # Parse the response
    lines = analysis.strip().split('\n')
    score = "N/A"
    matched = ""
    missing = ""
    verdict = ""
    
    for line in lines:
        if line.startswith("SCORE:"):
            score = line.replace("SCORE:", "").strip()
        elif line.startswith("MATCHED_SKILLS:"):
            matched = line.replace("MATCHED_SKILLS:", "").strip()
        elif line.startswith("MISSING_SKILLS:"):
            missing = line.replace("MISSING_SKILLS:", "").strip()
        elif line.startswith("VERDICT:"):
            verdict = line.replace("VERDICT:", "").strip()

    # Display score
    st.markdown("---")
    score_num = int(''.join(filter(str.isdigit, score))) if any(c.isdigit() for c in score) else 0
    
    if score_num >= 70:
        st.success(f"## ✅ Match Score: {score}/100")
    elif score_num >= 40:
        st.warning(f"## ⚠️ Match Score: {score}/100")
    else:
        st.error(f"## ❌ Match Score: {score}/100")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### ✅ Your Matching Skills")
        for skill in matched.split(','):
            st.markdown(f"- {skill.strip()}")
    
    with col4:
        st.markdown("### ❌ Skills You're Missing")
        for skill in missing.split(','):
            st.markdown(f"- {skill.strip()}")

    st.markdown(f"**💬 Verdict:** {verdict}")

    # Generate cover letter
    st.markdown("---")
    with st.spinner("Writing your cover letter..."):
        cover_prompt = f"""Write a professional, compelling cover letter for this job application. 
Make it specific to the job description and highlight relevant experience from the resume.
Keep it under 300 words. Sound human and enthusiastic, not robotic.

Job Description:
{job_description}

Resume:
{resume}"""

        cover_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": cover_prompt}]
        )
        cover_letter = cover_response.choices[0].message.content

    st.markdown("### 📝 Your Custom Cover Letter")
    st.text_area("Copy this cover letter:", cover_letter, height=300)
    st.success("✅ Done! Copy your cover letter above.")