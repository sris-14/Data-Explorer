import streamlit as st
import pandas as pd
import requests
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# FastAPI endpoint
# FASTAPI_URL = "http://127.0.0.1:8000"
FASTAPI_URL = "https://data-explorer-i7nf.onrender.com"
st.set_page_config(page_title=" Data Explorer", layout="wide")

st.title("Data Explorer & CSV Analyzer")

# Section 1: Display Sample Olympic Data (from FastAPI)
st.header("📌 Sample Olympic Data (from FastAPI)")

option = st.selectbox("Choose Data to View:", ["Athletes", "Medals"])

if option == "Athletes":
    country = st.text_input("Enter Country NOC (e.g., USA, IND, CHN):")
    
    if st.button("Fetch Athletes"):
        if country:
            with st.spinner("Fetching data..."):
                try:
                    response = requests.get(f"{FASTAPI_URL}/athletes?country={country}")
                    response.raise_for_status()
                    data = response.json().get('athletes', [])

                    # Ensure data is a list
                    df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])

                    if not df.empty:
                        st.dataframe(df)  # Enhanced UI (sortable, scrollable)
                    else:
                        st.warning("No data found for this country!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching data: {e}")
        else:
            st.warning("⚠️ Please enter a country code!")

elif option == "Medals":
    year = st.number_input("Enter Year (e.g., 2000, 2016):", min_value=1896, max_value=2024, step=4)

    if st.button("Fetch Medals"):
        with st.spinner("Fetching data..."):
            try:
                response = requests.get(f"{FASTAPI_URL}/medals?year={year}")
                response.raise_for_status()
                data = response.json().get('medal_data', [])

                # Ensure data is a list
                df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])

                if not df.empty:
                    st.dataframe(df)
                else:
                    st.warning("No medal data found for this year!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")

# Section 2: Upload and Analyze CSV Files
st.header("📊 Upload Your CSV for Analysis")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    st.subheader("📂 Uploaded Data Preview")
    
    df_uploaded = pd.read_csv(uploaded_file)
    st.dataframe(df_uploaded.head())  # Scrollable, filterable table

    # Show basic statistics before full profiling
    st.subheader("📊 Basic Statistics")
    st.write(df_uploaded.describe())

    # Generate profiling report
    if st.button("Generate Profiling Report"):
        with st.spinner("Generating Report..."):
            profile = ProfileReport(df_uploaded, explorative=True)
            st_profile_report(profile)
