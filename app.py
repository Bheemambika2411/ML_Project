from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2
from PyPDF2 import PdfReader
# Load environment variables from .env
load_dotenv()
# Configure Streamlit
st.set_page_config(
    page_title="Generative AI Text Summarization Blog",
    page_icon="📄",
    layout="wide"
)
# Custom CSS for better styling
st.markdown("""
    <style>
        body {
            background-color: #000000; /* Light grey background */
            color: #333333; /* Dark grey text */
            font-family: Arial, sans-serif; /* Font style */
        }
        .header {
            background-color: #000000; /* Dark blue header */
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .footer {
            background-color: #000000; /* Dark blue footer */
            color: white;
            padding: 10px;
            text-align: center;
            border-radius: 10px;
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
        }
        .summary-btn {
            background-color:#000000; /* Dark blue button */
            color: white;
            border: none;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 8px 4px;
            cursor: pointer;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .summary-btn:hover {
            background-color:#000000; /* Darker blue on hover */
        }
        .blog-content {
            background-color: #ffffff; /* White background for content */
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .blog-title {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .blog-text {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Configure Google Generative AI
genai.configure(api_key=os.getenv("YOUR API KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to generate summary
def summarize(text, style):
    if style == "Brief":
        prompt = f"Give a brief summary of the following text: {text}"
    elif style == "Detailed":
        prompt = f"Provide a detailed summary of the following text: {text}"
    elif style == "Key Points":
        prompt = f"Summarize the following text with key points: {text}"
    
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Streamlit app layout as a blog website
st.markdown('<div class="header"><h1 style="color: white;">YOUR AI CHATBOT</h1></div>', unsafe_allow_html=True)

# Blog introduction section
st.markdown(
    """
    <div class="blog-content">
        <h2 class="blog-title">Introduction</h2>
        <p class="blog-text">Welcome to the Generative AI Text Summarization Blog! In this blog, we explore various aspects of text summarization using generative AI models. 
        Upload a PDF, select how you want it summarized, and let the model generate a summary for you. You can also ask questions about the text and get answers based on the content.</p>
    <h3> Lets Make learning More intresting with YOUR AI CHATBOT</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# User input for text with a larger textarea
input_text = st.text_area('Input your text here:', height=300)

# File uploader for PDFs
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Extract text from PDF if uploaded
if uploaded_file is not None:
    input_text = extract_text_from_pdf(uploaded_file)
    st.markdown(
        f"""
        <div class="blog-content">
            <h2 class="blog-title">Extracted Text from PDF</h2>
            <p class="blog-text">{input_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Buttons for summarization style selection
col1, col2, col3 = st.columns(3)
if st.button('Get Brief Summary', key='brief', help='Get a brief summary'):
    summary_text = summarize(input_text, "Brief")
    st.markdown(
        f"""
        <div class="blog-content">
            <h2 class="blog-title">Generated Brief Summary</h2>
            <p class="blog-text">{summary_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
if st.button('Get Detailed Summary', key='detailed', help='Get a detailed summary'):
    summary_text = summarize(input_text, "Detailed")
    st.markdown(
        f"""
        <div class="blog-content">
            <h2 class="blog-title">Generated Detailed Summary</h2>
            <p class="blog-text">{summary_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
if st.button('Get Key Points Summary', key='keypoints', help='Get key points summary'):
    summary_text = summarize(input_text, "Key Points")
    st.markdown(
        f"""
        <div class="blog-content">
            <h2 class="blog-title">Generated Key Points Summary</h2>
            <p class="blog-text">{summary_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
# Text input for queries related to the PDF
query_text = st.text_input("Ask a question about the text:")
if query_text:
    response = model.generate_content(f"Based on the following text: {input_text}, answer this question: {query_text}")
    st.markdown(
        f"""
        <div class="blog-content">
            <h2 class="blog-title">Answer to Your Question</h2>
            <p class="blog-text">{response.text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Footer
st.markdown('<div class="footer">Generative AI Text Summarization Blog by Ambika Bolli</div>', unsafe_allow_html=True)
