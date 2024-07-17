import streamlit as st

from services.document_service import DocumentService
cn = st.connection("rag_db", type="sql")
document_service = DocumentService(cn)

from services.vectorstore_service import VectorStoreService
vectorstore_service = VectorStoreService()

st.header("Court documents")

st.write("Here you can view and upload new documents to further search and aggregate information on them.")

st.header("Uploading new court documents")
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=".pdf"
)
if uploaded_file is not None:
    with st.spinner('Processing the document...'):
        doc_pk, path = document_service.upload_document(
            uploaded_file.name,
            uploaded_file.getbuffer()
        )
        vectorstore_service.load_document(doc_pk, path)
    st.success('Done!')

st.header("List of court documents")
st.table(document_service.get_uploaded_files())