import streamlit as st
from main import ocr
st.set_page_config(page_title="Vision AI", page_icon="📖", layout="wide")
st.header("👁️ Vision AI")

uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt", "jpg", "png"],
    help="Scanned documents are now supported yet!",
)

if uploaded_file is not None:
    with st.spinner('Processing...'):
        print(uploaded_file)
        url = "https://document-intelligence-service-new.cognitiveservices.azure.com/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2023-07-31"
        response = ocr(url)
        st.markdown(response)