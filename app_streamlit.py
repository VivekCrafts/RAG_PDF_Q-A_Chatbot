import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/ask"  # change if your FastAPI is on another port

st.set_page_config(page_title="PDF Q&A", layout="wide")
st.title("📄 Transformer Paper Q&A")
st.markdown("Ask questions about your Transformer paper PDF!")

# Input box
question = st.text_input("Enter your question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            # Call FastAPI
            response = requests.post(API_URL, json={"question": question})
            if response.status_code == 200:
                data = response.json()
                st.subheader("Answer:")
                st.success(data["answer"])

            else:
                st.error(f"Error {response.status_code}: {response.json().get('detail')}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
