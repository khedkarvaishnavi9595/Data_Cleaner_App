import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Cleaning & Visualization App", layout="wide")

st.title("📊 Data Cleaning & Visualization Tool")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("🔍 Raw Data Preview")
    st.dataframe(df)

    # Data Summary
    st.subheader("📌 Data Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Duplicate Rows", df.duplicated().sum())

    # Null Values
    st.subheader("⚠️ Missing Values")
    st.write(df.isnull().sum())

    # ---------------- CLEANING OPTIONS ----------------
    st.sidebar.header("🧹 Data Cleaning Options")

    # Remove duplicates
    if st.sidebar.checkbox("Remove Duplicate Rows"):
        df = df.drop_duplicates()
        st.success("Duplicate rows removed")

    # Handle missing values
    if st.sidebar.checkbox("Fill Missing Values"):
        fill_method = st.sidebar.selectbox(
            "Select Fill Method",
            ["Mean", "Median", "Mode", "Forward Fill"]
        )

        if fill_method == "Mean":
            df = df.fillna(df.mean(numeric_only=True))
        elif fill_method == "Median":
            df = df.fillna(df.median(numeric_only=True))
        elif fill_method == "Mode":
            df = df.fillna(df.mode().iloc[0])
        elif fill_method == "Forward Fill":
            df = df.fillna(method="ffill")

        st.success(f"Missing values filled using {fill_method}")

    st.subheader("✅ Cleaned Data Preview")
    st.dataframe(df)

    #  VISUALIZATION
    st.subheader("📈 Data Visualization")

    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if numeric_columns:
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Bar Chart", "Line Chart", "Histogram"]
        )

        selected_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        fig, ax = plt.subplots()

        if chart_type == "Bar Chart":
            ax.bar(df.index, df[selected_column])
        elif chart_type == "Line Chart":
            ax.plot(df[selected_column])
        elif chart_type == "Histogram":
            ax.hist(df[selected_column], bins=20)

        ax.set_title(f"{chart_type} - {selected_column}")
        st.pyplot(fig)

    else:
        st.warning("No numeric columns available for visualization.")

    st.subheader("⬇️ Download Cleaned Data")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download as CSV",
        csv,
        "cleaned_data.csv",
        "text/csv"
    )
