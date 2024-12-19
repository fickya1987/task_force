import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app title
st.title("AI-Enhanced Data Analysis and Visualization")

# File upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file:", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read the file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("### Uploaded Data Table")
        st.dataframe(df, use_container_width=True)

        # Interactive data visualization and search
        st.write("### Interactive Table View")
        search_term = st.text_input("Search in table:")
        if search_term:
            filtered_data = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        else:
            filtered_data = df

        st.dataframe(filtered_data, use_container_width=True)

        # GPT-4o Integration for Analysis
        st.subheader("Data Analysis with GPT-4o")
        analysis_query = st.text_area("Enter analysis description or query details:")
        analysis_type = st.radio("Choose GPT-4o Analysis Type:", ["Data-Based Analysis", "Global GPT-4o Search"])

        if st.button("Generate AI Analysis") and analysis_query:
            try:
                if analysis_type == "Data-Based Analysis":
                    # Data-based analysis
                    prompt_data = f"Perform an in-depth analysis of '{analysis_query}' based on the following data:\n{filtered_data.to_csv(index=False)}"
                    response_data = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are an experienced data analyst. Use Indonesian."},
                            {"role": "user", "content": prompt_data}
                        ],
                        max_tokens=2048,
                        temperature=1.0
                    )
                    result_data = response_data['choices'][0]['message']['content']
                    st.write("#### Data-Based Analysis Result:")
                    st.write(result_data)
                else:
                    # Global GPT-4o search
                    prompt_search = f"Conduct an in-depth search on '{analysis_query}' using your global knowledge."
                    response_search = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are an intelligent search engine. Use Indonesian."},
                            {"role": "user", "content": prompt_search}
                        ],
                        max_tokens=2048,
                        temperature=1.0
                    )
                    result_search = response_search['choices'][0]['message']['content']
                    st.write("#### Global GPT-4o Search Result:")
                    st.write(result_search)
            except Exception as e:
                st.error(f"Error generating analysis: {e}")

    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.warning("No file uploaded. Please upload a CSV or Excel file.")
