import streamlit as st 
import pdfplumber
import os
from anthropic import Anthropic
from langchain.text_splitter import CharacterTextSplitter

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        with pdfplumber.open(pdf) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    return text


def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


st.set_page_config(
    page_title="Proposal Summarizer",
    page_icon="📄",
)

st.title("RFP Insights")

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

with st.sidebar:
    st.subheader("Your Documents")
    pdf_docs = st.file_uploader("Upload your pdf's here and click on Process",accept_multiple_files=True)
    if st.button("Process"):
        with st.spinner("Summarizing your documents..."):
            raw_text = get_pdf_text(pdf_docs)
            text_chunks = get_text_chunks(raw_text)
            
