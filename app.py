import streamlit as st
import json
import pandas as pd
from generate_report import create_pdf_report

st.set_page_config(layout="wide")
st.title("Dynamic PDF Report Generator")

uploaded_file = st.file_uploader("Upload JSON data file", type=["json"])

if uploaded_file:
    data = json.load(uploaded_file)
    df = pd.DataFrame(data).T.drop(columns='average_score')
    st.write("### Preview of Data")
    st.dataframe(df)

    if st.button("Generate PDF Report"):
        create_pdf_report(data)
        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, file_name="report.pdf")

