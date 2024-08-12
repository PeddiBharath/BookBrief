import streamlit as st
from openai import OpenAI
from functions import get_chunks

st.title("Book Brief")

st.markdown("""
            <h3>Summarise any book</h3>
            """,unsafe_allow_html=True)

with st.sidebar:
    api_key = st.text_input(
        label="Enter your OpenAI key",
        type="password",
        help=(
                    """Obtain your key from the OpenAI website, 
                    then paste it into the "Enter Your OpenAI Key" section on our site and click "Save" or "Submit."
                    If you encounter any issues, please contact our support team for assistance."""
                )
        )
    words = st.slider(
        label="Words",
        value=300,
        min_value=50,
        max_value=5000,
        step=50,
        help=(
                """Summary should have these many words"""
            )
        )
    
client = OpenAI(api_key=api_key)

file = st.file_uploader(label="Choose File",type="pdf")

global curr_summary
curr_summary = ""

if file and not api_key:
    st.warning("Enter the OpenAI key")

if file and api_key:
    chunks = get_chunks(file)
    past_summary = ""
    for chunk in chunks:
        prompt = f"This is the past summary {past_summary} and this the new chunk is {chunk}. Generate the summary using it."
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an excellent summary generator. It is **MANDATORY** that the summary is exactly {words} words long. The summary must be exactly {words} words; this is **VERY IMPORTANT**."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0
        )
        curr_summary = response.choices[0].message.content.strip()
        past_summary = curr_summary
    st.markdown("""
                <h3>The Summary is:</h3>
                """,unsafe_allow_html=True)
    st.write(curr_summary)

