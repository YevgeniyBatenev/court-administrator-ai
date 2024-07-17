import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import AzureOpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector


class VectorStoreService:

    def __init__(self):
        self._embeddings = AzureOpenAIEmbeddings(
            model=st.secrets.openai.embeddings_model,
            azure_endpoint=st.secrets.openai.azure_openai_endpoint,
            api_version=st.secrets.openai.openai_api_version,
            api_key=st.secrets.openai.openai_api_key,
        )
        self._vectorstore = PGVector(
            embeddings=self._embeddings,
            collection_name=st.secrets.rag_vectorstore.collection_name,
            connection=st.secrets.rag_vectorstore.url,
            use_jsonb=True,
        )

    def load_document(self, pk: int, path: str):
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        for page in pages:
            page.page_content = page.page_content.replace("\x00", "\uFFFD")
            page.metadata.update(document_pk=pk)
        self._vectorstore.add_documents(pages)

    def get_retriever(self) -> VectorStoreRetriever:
        return self._vectorstore.as_retriever(search_type="mmr")