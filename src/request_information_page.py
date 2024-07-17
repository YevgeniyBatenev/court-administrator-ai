import streamlit as st

from services.rag_service import RAGService
from services.vectorstore_service import VectorStoreService

vectorstore_service = VectorStoreService()
rag_service = RAGService(vectorstore_service.get_retriever())

st.header("Request information about court cases")

st.write(
    """The main task of this mini project is to obtain aggregated and formulated data using AI based on downloaded files containing information about court cases."""
)

request_query = st.text_input("Enter your request query 👇")
if request_query:
    with st.spinner('Working on the request...'):
        answer = rag_service.request_information(request_query)
        st.write(f"Answer: {answer}")
