from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2  # Import PyPDF2 for PDF processing

# Load Google API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Load model (adjust model name as needed)
model = genai.GenerativeModel("gemini-pro")

# Load PDF knowledge base
with open("/Users/arhambafna/GEMINIAPI/Finrules.pdf", "rb") as pdf_file:  # Replace with your PDF path
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

st.title("Q&A Bot with Generative AI (Knowledge Base Enhanced)")
st.subheader("Hello! How can I assist you today?")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question or make a request:"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response using Generative AI
    try:
        response = model.generate_content(prompt)
        response = response.text # Extract text content
    except Exception as e:
        response = f"Error generating response: {str(e)}"

    # Display generative AI response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
