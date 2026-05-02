import streamlit as st
import pandas as pd
import numpy as np

st.title("Driver Pay Insight Tool")

uploaded_file = st.file_uploader("Upload payroll report")

if uploaded_file:

    df = pd.read_excel(uploaded_file, header=3)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    df = df.rename(columns={df.columns[1]: "Driver Name"})

    PAY = "Pay Amt"
    df[PAY] = pd.to_numeric(df[PAY], errors='coerce')

    st.subheader("Summary")
    st.write("Total Pay:", df[PAY].sum())
    st.write("Average Pay:", df[PAY].mean())

    st.subheader("Top Drivers")
    top = df.sort_values(by=PAY, ascending=False).head(5)
    st.dataframe(top[["Driver", "Driver Name", PAY]])

    df["Stops"] = df["Stops"].replace(0, np.nan)
    df["Pay per Stop"] = df[PAY] / df["Stops"]

    st.subheader("High Cost Drivers")
    inefficient = df.sort_values(by="Pay per Stop", ascending=False).head(5)
    st.dataframe(inefficient[["Driver Name", "Pay per Stop"]])

    problem = df[(df["Stops"].isna()) & (df[PAY] > 0)]

    st.subheader("Data Issues (Pay with 0 Stops)")
    st.dataframe(problem[["Driver Name", PAY]])