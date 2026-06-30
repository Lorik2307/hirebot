#  HireBot — AI Job Application Assistant

An AI-powered tool that analyzes your resume against any job description.

## What it does
- 📊 Scores how well you match a job (0-100%)
- ✅ Lists your matching skills
- ❌ Shows skills you're missing
- 📝 Writes a custom cover letter for you
- 📄 Supports PDF resume upload

## Tech Stack
- Python
- Streamlit
- Groq API (Llama 3.1)
- PyPDF2

## How to run
1. Clone the repo
2. Run `pip install streamlit groq PyPDF2 python-dotenv`
3. Add your Groq API key to a `.env` file as `GROQ_API_KEY=your_key`
4. Run `streamlit run app.py`
