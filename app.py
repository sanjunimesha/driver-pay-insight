import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Driver Pay Insights", layout="wide")

# Title
st.title("🚚 Driver Pay Insight Dashboard")
st.markdown("Upload weekly payroll reports to identify cost drivers, inefficiencies, and anomalies.")

# Upload file
uploaded_file = st.file_uploader("Upload payroll report")

# Main logic
if uploaded_file:

    # Load and clean data
    df = pd.read_excel(uploaded_file, header=3)
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    df = df.rename(columns={df.columns[1]: "Driver Name"})

    # Filter
    driver_filter = st.text_input("🔍 Search Driver Name")

    if driver_filter:
        df = df[df["Driver Name"].str.contains(driver_filter, case=False, na=False)]

    # Pay calculations
    PAY = "Pay Amt"
    df[PAY] = pd.to_numeric(df[PAY], errors='coerce')

    # Summary
    st.subheader("📊 Summary")
    st.write("Total Pay:", df[PAY].sum())
    st.write("Average Pay:", df[PAY].mean())

    # Top drivers
    st.subheader("🚨 Top Cost Drivers")
    top = df.sort_values(by=PAY, ascending=False).head(5)
    st.dataframe(top[["Driver", "Driver Name", PAY]])

    # Efficiency
    df["Stops"] = pd.to_numeric(df["Stops"], errors='coerce')
    df["Stops"] = df["Stops"].replace(0, np.nan)
    df["Pay per Stop"] = df[PAY] / df["Stops"]

    st.subheader("⚙️ Inefficiencies (High Cost per Stop)")
    inefficient = df.sort_values(by="Pay per Stop", ascending=False).head(5)
    st.dataframe(inefficient[["Driver Name", "Pay per Stop"]])

    # Data issues
    problem = df[(df["Stops"].isna()) & (df[PAY] > 0)]

    st.subheader("⚠️ Data Issues (Pay without Stops)")
    st.dataframe(problem[["Driver Name", PAY]])

    # Insights
    st.subheader("🧠 Key Insights")

    total_drivers = len(df)
    problem_count = len(problem)

    st.write(f"- Total drivers analyzed: {total_drivers}")
    st.write(f"- {problem_count} drivers have pay recorded but zero stops")

    if problem_count > 0:
        st.warning("Potential data inconsistency detected: Some drivers are paid without recorded activity")

    avg_pps = df["Pay per Stop"].mean()
    high_cost = df[df["Pay per Stop"] > avg_pps * 1.5]

    st.write(f"- {len(high_cost)} drivers have unusually high cost per stop")

    if len(high_cost) > 0:
        st.warning("Inefficiency detected: Some drivers are significantly more expensive per stop")

    # Download button (always visible)
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇️ Download Processed Data",
        csv,
        "processed_data.csv",
        "text/csv"
    )
