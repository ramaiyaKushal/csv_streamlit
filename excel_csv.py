import streamlit as st
import pandas as pd

# Title of the app
st.title('Excel to CSV Converter')

# Upload Excel file
uploaded_file = st.file_uploader("Choose a file", type=["xls", "xlsx"])

if uploaded_file is not None:
    option = st.selectbox(
    "Which Bank is it?",
    ("ICICI Bank", "SBI Bank", "Axis Bank"),
    index=None,
    placeholder="Select a bank",
    )
    if option is not None:
        st.write("You selected:", option)
        if option == "ICICI Bank":
            df = pd.read_excel(uploaded_file,skiprows=6)
        elif option == "Axis Bank":
            df = pd.read_excel(uploaded_file, skiprows=13).dropna(how='all', axis=1)
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])
            df.columns = [col.strip() for col in df.columns]  # remove any leading/trailing whitespaces in column names
            df = df.rename(columns={'DR|CR': 'Cr/Dr'})
        elif option == "SBI Bank":
            df = None

        # Modify the dataframe here as per your requirement
        # For example, let's assume we're dropping a column named 'Unnamed: 0'
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
        
        df['Transaction Amount(INR)'] = df.apply(lambda row: -1 * row['Transaction Amount(INR)'] if row['Cr/Dr'] == 'DR' else row['Transaction Amount(INR)'], axis=1)
        
        # Write to CSV
        csv = df.to_csv(index=False)
        st.write("Modified CSV")
        st.write(df)

        # Download CSV file
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='modified_data.csv',
            mime='text/csv',
        )
