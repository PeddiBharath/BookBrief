from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

def get_chunks(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=3500,
        chunk_overlap=300,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks