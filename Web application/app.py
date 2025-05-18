# app.py
import streamlit as st
import pandas as pd
from rfm_model import compute_rfm

st.set_page_config(page_title="RFM Analysis App", layout="wide")
st.title("Customer Segmentation using RFM Model")

uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    with st.form("rfm_form"):
        st.write("### Select Relevant Columns")
        customer_col = st.selectbox("Customer ID Column", df.columns)
        date_col = st.selectbox("Transaction Date Column", df.columns)
        amount_col = st.selectbox("Revenue/Amount Column", df.columns)
        submitted = st.form_submit_button("Run RFM Analysis")

    if submitted:
        try:
            rfm_result = compute_rfm(df, customer_col, date_col, amount_col)
            st.success("RFM Analysis Completed!")

            st.subheader("RFM Table")
            st.dataframe(rfm_result)

            csv = rfm_result.to_csv(index=True).encode('utf-8')
            st.download_button("Download RFM Results as CSV", data=csv, file_name="rfm_results.csv", mime="text/csv")
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
else:
    st.info("Please upload a CSV file to get started.")
