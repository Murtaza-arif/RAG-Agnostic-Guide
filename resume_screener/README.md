# Resume Screener

An AI-powered resume screening application that uses LlamaIndex and OpenAI to analyze resumes against job descriptions.

## Setup and Installation

### Using Conda (Recommended)
1. Create and activate the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate resume-screener
   ```

## Running the Application

Run the Streamlit application:
```bash
streamlit run resume_screener.py
```

## Features

- Upload PDF resumes
- Input job descriptions
- Get AI-powered analysis of candidate fit
- Detailed breakdown of skills and experiences
- Gap analysis
- Numerical rating of candidate suitability

## Technologies Used

- LlamaIndex for document processing and RAG
- OpenAI for embeddings and analysis
- Streamlit for the user interface
- PyPDF for PDF processing

## How it Works

1. Upload a PDF resume through the Streamlit interface
2. Enter the job description you want to screen against
3. The application will:
   - Extract text from the PDF
   - Create embeddings using OpenAI
   - Use LlamaIndex to process and analyze the content
   - Generate a comprehensive analysis of the candidate's fit
   - Provide detailed feedback and ratings

## Note

Make sure you have a valid OpenAI API key set in your `.env` file before running the application.
