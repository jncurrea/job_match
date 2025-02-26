import streamlit as st
import pdfplumber
import docx2txt
import json
import openai
from openai import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import os
os.environ["OPENAI_API_KEY"] = "your_api_key"
# Initialize OpenAI client
client = OpenAI()

# Function to extract text from resume
def extract_resume_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(uploaded_file)
    else:
        return None

# Function to get embeddings
embeddings = OpenAIEmbeddings()

def get_text_embedding(text):
    return embeddings.embed_query(text)

# Function to compute match score
def calculate_match_score(resume_text, jd_text):
    resume_embedding = get_text_embedding(resume_text)
    jd_embedding = get_text_embedding(jd_text)
    match_score = cosine_similarity([resume_embedding], [jd_embedding])[0][0]
    return round(match_score * 100, 2)

# LLM context for GPT-4
llm_context = """
You are an experienced headhunter specializing in helping early-career and associate-level professionals
optimize their resumes for job applications. Your goal is to analyze a candidate's resume and compare it to
a job description to provide insightful recommendations.

Your output should be structured as follows:

{
  "key_strengths": [
    "Highlight relevant skills & experiences in the resume, focusing on alignment with the job description."
  ],
  "missing_skills": [
    "Identify critical missing skills based on the JD, prioritizing technical skills, tools, or industry-specific knowledge."
  ],
  "recommendations": [
    "Provide specific suggestions on improving the resume. Include example modifications such as what bullet point to update and how it should be reworded."
  ],
  "Sample_cover_letter": [
    "Provide a sample cover letter that the candidate can use as a reference. You highlight how the candidate's experience aligns with the job requirements and mostly with the preferred skills or preferred qualifications.
    Cover letter must have 3 to 4 paragraphs where following this template:
    
    To whom it may concern,

    Opening paragraph: Clearly state why you're writing, name the position or type of work you're exploring and, 
    where applicable, how you heard about the position or organization. A summary statement
    may work well here by including three reasons you think you would be a good fit for the opportunity.

    Middle paragraph(s): Explain why you are interested in this employer
    and your reasons for desiring this type of work. If you've had relevant
    school or work experience, be sure to point it out with one or two key
    examples; but do not reiterate your entire resume. Emphasize skills or
    abilities that relate to the job. Be sure to do this in a confident manner
    and remember that the reader will view your letter as an example of
    your writing skills.

    Closing paragraph: Reiterate your interest in the position, and
    your enthusiasm for using your skills to contribute to the work
    of the organization. Thank the reader for their consideration of
    your application, and end by stating that you look forward to the
    opportunity to further discuss the position.

    Sincerely,
    Your name typed"
  ]
}

Use clear, professional, and motivating language. Avoid generic terms and focus on industry-specific skills.
Your output should be worded towards the candidate using phrases such as:
- 'You should consider adding...'
- 'Your resume would benefit from including...'
- 'It may be helpful to highlight your experience with...'

Ensure the response is a **valid JSON object** with no additional text.
STRICT RULE: Do not include extra commentary, explanations, or markdown formatting. ONLY return the JSON response.
"""

# Function to analyze resume using GPT-4
# Function to analyze resume using GPT-4
def analyze_resume_with_llm(resume_text, jd_text):
    prompt = f"""
    {llm_context}

    Candidate's Resume:
    {resume_text}

    Job Description:
    {jd_text}

    Analyze the resume based on the job description and return the structured JSON response.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",  # ✅ Use GPT-4-turbo version
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}  # ✅ Only works with turbo models!
        )

        llm_output = response.choices[0].message.content.strip()
        return llm_output  # GPT-4-turbo already returns JSON, so no need to parse

    except openai.BadRequestError as e:
        # 🔴 If model does not support JSON formatting, fallback to text parsing
        if "response_format" in str(e):
            print("Model does not support structured JSON. Switching to text-based parsing.")

            response = client.chat.completions.create(
                model="gpt-4",  # Fallback to regular GPT-4
                messages=[{"role": "user", "content": prompt}]
            )

            llm_output = response.choices[0].message.content.strip()

            # 🛠️ Manually enforce JSON parsing for models that don't support `response_format`
            try:
                parsed_response = json.loads(llm_output)
                return parsed_response
            except json.JSONDecodeError:
                st.error("🚨 Error: LLM response is not valid JSON. Please try again.")
                return None

        else:
            raise e  # Raise any other OpenAI errors


# Streamlit UI
st.set_page_config(page_title="Resume Matcher", page_icon="📄", layout="wide")

st.title("📄 Resume & Job Description Matcher")
st.write("Upload your resume (PDF or DOCX) and paste a job description to see how well they match.")

# File uploader for resume
uploaded_resume = st.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf", "docx"])

# Text area for job description
jd_text = st.text_area("Paste the job description here", height=300)

# Match button
if st.button("Analyze Resume"):
    if uploaded_resume is None:
        st.warning("⚠️ Please upload your resume.")
    elif not jd_text.strip():
        st.warning("⚠️ Please paste the job description.")
    else:
        # Extract text from resume
        resume_text = extract_resume_text(uploaded_resume)
        if not resume_text.strip():
            st.error("🚨 Error extracting text from the resume. Please try another file.")
        else:
            with st.spinner("⏳ Analyzing..."):
                # Calculate match score
                match_score = calculate_match_score(resume_text, jd_text)

                # Get structured response from LLM
                parsed_response = analyze_resume_with_llm(resume_text, jd_text)

                if parsed_response:
                    if isinstance(parsed_response, str):  # Ensure it's a valid dictionary
                        try:
                            parsed_response = json.loads(parsed_response)  # Convert JSON string to dictionary
                        except json.JSONDecodeError:
                            st.error("🚨 Error: LLM response is not valid JSON. Please try again.")
                            parsed_response = {}
                    key_strengths = parsed_response.get("key_strengths", [])
                    missing_skills = parsed_response.get("missing_skills", [])
                    recommendations = parsed_response.get("recommendations", [])
                    sample_cover_letter = parsed_response.get("Sample_cover_letter", [])

                    # Display results
                    st.subheader(f"✅ Match Score: {match_score}%")
                    
                    st.subheader("💪 Key Strengths")
                    for strength in key_strengths:
                        st.write(f"- {strength}")

                    st.subheader("🔍 Missing Skills")
                    if missing_skills:
                        for skill in missing_skills:
                            st.write(f"- {skill}")
                    else:
                        st.write("✅ No missing skills detected!")

                    st.subheader("💡 Recommendations")
                    for recommendation in recommendations:
                        st.write(f"- {recommendation}")

                    st.subheader("💼 Sample Cover Letter")
                    if sample_cover_letter:
                        st.write(f"- {sample_cover_letter}")
                    else:
                        st.write("✅ No sample cover letter provided.")
