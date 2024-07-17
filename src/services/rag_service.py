import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import AzureChatOpenAI


class RAGService:
    def __init__(self, retriever: VectorStoreRetriever):
        self._retriever = retriever
        self._llm_with_params = AzureChatOpenAI(
            openai_api_key=st.secrets.openai.openai_api_key,
            openai_api_version=st.secrets.openai.openai_api_version,
            azure_endpoint=st.secrets.openai.azure_openai_endpoint,
            model=st.secrets.openai.openai_model,
            temperature=st.secrets.openai.temperature,
            max_tokens=st.secrets.openai.max_tokens,
        )

    @property
    def _template(self):
        return """Answer the question based only on the following context:
            {context}

            Question: {question}"""

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    def request_information(self, request: str) -> str:
        prompt = PromptTemplate(
            template=self._template,
            input_variables=["context", "question"]
        )

        rag_chain = (
                {"context": self._retriever | self._format_docs, "question": RunnablePassthrough()}
                | prompt
                | self._llm_with_params
                | StrOutputParser()
        )
        rag_result = rag_chain.invoke(request)
        return rag_result