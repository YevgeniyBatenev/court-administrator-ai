import streamlit as st


request_information_page = st.Page(
    "request_information_page.py",
    title="Request information",
    icon=":material/quick_reference_all:"
)

documents_page = st.Page(
    "documents_page.py",
    title="Documents",
    icon=":material/list:"
)


pg = st.navigation([request_information_page, documents_page])

st.set_page_config(page_title="Court Administrator", page_icon=":material/gavel:")

pg.run()
