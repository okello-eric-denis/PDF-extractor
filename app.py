import streamlit as st
import fitz  # PyMuPDF
import pandas as pd

# App title
st.title("PDF Text Extractor App")

# Layout: Columns for upload and options
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Upload Your PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

with col2:
    st.header("Options")
    download_format = st.radio("Download format:", ["TXT", "CSV"])

# State management and processing logic
if uploaded_file is not None:
    with st.spinner("Processing your file..."):
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        extracted_text = ""

        # Extract text from all pages in the PDF
        for page in pdf_document:
            extracted_text += page.get_text()

        pdf_document.close()

        # Display success message and extracted text
        st.success("File processed successfully!")
        with st.expander("Extracted Text"):
            st.write(extracted_text)

        # Prepare download options
        if download_format == "TXT":
            st.download_button(
                label="Download as TXT",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        elif download_format == "CSV":
            text_data = pd.DataFrame({"Extracted Text": [extracted_text]})
            csv_data = text_data.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv_data,
                file_name="extracted_text.csv",
                mime="text/csv"
            )
