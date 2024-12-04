import streamlit as st
from llama_index.core.llama_pack import download_llama_pack
from pathlib import Path
import tempfile
import os
import time

from dotenv import load_dotenv

load_dotenv()
# Initialize session state for ResumeScreenerPack
if 'resume_screener_pack' not in st.session_state:
    st.session_state.resume_screener_pack = None

def initialize_resume_screener():
    if st.session_state.resume_screener_pack is None:
        try:
            ResumeScreenerPack = download_llama_pack("ResumeScreenerPack", "./resume_screener_pack")
            st.session_state.resume_screener_pack = ResumeScreenerPack
        except Exception as e:
            st.error(f"Error initializing Resume Screener: {str(e)}")
            return None
    return st.session_state.resume_screener_pack

def check_openai_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("""
        OpenAI API key not found! Please set your OPENAI_API_KEY in a .env file.
        
        1. Create a .env file in the project directory
        2. Add the following line:
           OPENAI_API_KEY=your_api_key_here
        
        You can get your API key from: https://platform.openai.com/api-keys
        """)
        return False
    return True

def analyze_resume_details(resume_file, job_description, criteria):
    if not check_openai_api_key():
        return None
        
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / resume_file.name
            with open(temp_path, 'wb') as f:
                f.write(resume_file.getvalue())
            
            ResumeScreenerPack = initialize_resume_screener()
            if ResumeScreenerPack is None:
                return None
                
            # Create a more detailed job analysis prompt
            detailed_analysis_prompt = f"""
            Analyze this resume against the job description and provide:
            1. Skills Assessment:
               - Technical Skills (rate each 1-5)
               - Soft Skills (rate each 1-5)
               - Domain Knowledge (rate each 1-5)
            
            2. Experience Analysis:
               - Years of relevant experience
               - Key achievements
               - Leadership roles
            
            3. Gap Analysis:
               - Missing required skills
               - Areas needing improvement
               - Suggested training/certifications
            
            4. Overall Rating:
               - Technical Fit (1-5)
               - Cultural Fit (1-5)
               - Experience Fit (1-5)
               - Overall Score (1-5)
            
            Job Description:
            {job_description}
            
            Required Criteria:
            {chr(10).join(f'- {c}' for c in criteria)}
            """
            
            resume_screener = ResumeScreenerPack(
                job_description=detailed_analysis_prompt,
                criteria=criteria
            )
            
            max_retries = 3
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    response = resume_screener.run(resume_path=str(temp_path))
                    return response
                except Exception as e:
                    if "APIConnectionError" in str(e) and attempt < max_retries - 1:
                        st.warning(f"Connection error, retrying in {retry_delay:.1f} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        raise e
                        
    except Exception as e:
        error_msg = str(e)
        if "APIConnectionError" in error_msg:
            st.error("""
            Failed to connect to OpenAI API. Please check:
            1. Your internet connection
            2. OpenAI API status: https://status.openai.com
            3. Your API key is valid
            
            Error details: """ + error_msg)
        else:
            st.error(f"Error analyzing resume: {error_msg}")
        return None

# Streamlit UI
st.title("Advanced Resume Screener")
st.write("Upload a resume and provide a job description for detailed AI-powered analysis")

# Job description input with example
example_jd = """We're looking for a Senior Machine Learning Engineer with:
- 5+ years of experience in ML/AI
- Strong Python programming skills
- Experience with deep learning frameworks
- Background in computer vision or NLP
- Team leadership experience
- Track record of delivering production ML systems"""

job_description = st.text_area(
    "Enter the job description:",
    height=200,
    help="Describe the job requirements and qualifications",
    placeholder=example_jd
)

# Criteria input with examples
st.subheader("Screening Criteria")
st.write("Add specific criteria to evaluate the candidate against")

example_criteria = [
    "5+ years of experience in machine learning or AI",
    "Proficiency in Python and ML frameworks",
    "Experience leading technical teams",
    "Track record of deploying ML systems to production",
    "Strong communication and collaboration skills"
]

criteria_list = []
num_criteria = st.number_input("Number of criteria", min_value=1, max_value=10, value=5)

for i in range(num_criteria):
    default_example = example_criteria[i] if i < len(example_criteria) else ""
    criterion = st.text_input(
        f"Criterion {i+1}",
        key=f"criterion_{i}",
        help=f"Enter specific requirement #{i+1}",
        placeholder=default_example
    )
    if criterion:
        criteria_list.append(criterion)

# Resume file upload
resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=['pdf'],
    help="Upload the candidate's resume in PDF format"
)

if st.button("Analyze Resume", help="Click to start the detailed analysis"):
    if not resume_file:
        st.warning("Please upload a resume file")
    elif not job_description:
        st.warning("Please enter a job description")
    elif not criteria_list:
        st.warning("Please add at least one screening criterion")
    else:
        with st.spinner("Performing detailed resume analysis..."):
            response = analyze_resume_details(resume_file, job_description, criteria_list)
            
            if response:
                st.subheader("Detailed Analysis Results")
                
                # Create tabs for different analysis sections
                tabs = st.tabs(["Skills Assessment", "Experience Analysis", "Gap Analysis", "Overall Rating"])
                
                with tabs[0]:  # Skills Assessment
                    st.markdown("### Skills Assessment")
                    st.write(response.overall_reasoning)
                    
                    # Display skills ratings if available in the response
                    if hasattr(response, 'criteria_decisions'):
                        for cd in response.criteria_decisions:
                            if "Technical Skills" in cd.reasoning or "Soft Skills" in cd.reasoning:
                                st.write(cd.reasoning)
                
                with tabs[1]:  # Experience Analysis
                    st.markdown("### Experience Analysis")
                    if hasattr(response, 'criteria_decisions'):
                        for cd in response.criteria_decisions:
                            if "experience" in cd.reasoning.lower():
                                st.write(cd.reasoning)
                
                with tabs[2]:  # Gap Analysis
                    st.markdown("### Gap Analysis")
                    if hasattr(response, 'criteria_decisions'):
                        gaps = [cd.reasoning for cd in response.criteria_decisions if not cd.decision]
                        if gaps:
                            for gap in gaps:
                                st.write("- " + gap)
                        else:
                            st.write("No significant gaps identified.")
                
                with tabs[3]:  # Overall Rating
                    st.markdown("### Overall Rating")
                    
                    # Display final decision with prominent styling
                    decision_color = "green" if response.overall_decision else "red"
                    decision_text = "✅ Recommended" if response.overall_decision else "❌ Not Recommended"
                    st.markdown(
                        f"<h2 style='text-align: center; color: {decision_color};'>{decision_text}</h2>",
                        unsafe_allow_html=True
                    )
                    
                    st.write("**Final Assessment:**")
                    st.write(response.overall_reasoning)
