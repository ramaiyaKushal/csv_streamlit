import streamlit as st
import pandas as pd
from io import StringIO
import tempfile

# Title of the app
st.title('Excel to CSV Converter')

# Upload Excel file
uploaded_file = st.file_uploader("Choose a file", type=["xls", "xlsx"])

if uploaded_file is not None:
    option = st.selectbox(
    "Which Bank is it?",
    ("ICICI Bank", "SBI Bank", "Axis Bank","Kotak Bank","Fincare Bank"),
    index=None,
    placeholder="Select a bank",
    )
    if option is not None:
        st.write("You selected:", option)
        if option == "ICICI Bank":
            df = pd.read_excel(uploaded_file,skiprows=6)
            st.write(df)
            df['Transaction Amount(INR)'] = df.apply(lambda row: -1 * row['Transaction Amount(INR)'] if row['Cr/Dr'] == 'DR' else row['Transaction Amount(INR)'], axis=1)
        
        elif option == "Axis Bank":
            df = pd.read_excel(uploaded_file, skiprows=13).dropna(how='all', axis=1)
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])
            df.columns = [col.strip() for col in df.columns]  # remove any leading/trailing whitespaces in column names
            # df = df.rename(columns={'DR|CR': 'Cr/Dr','Amount(INR)':'Transaction Amount(INR)'})
            df = df.dropna()
            st.write(df)
            df["Amount(INR)"] = df["Amount(INR)"].astype("float")
            df['Amount(INR)'] = df.apply(lambda row: -1 * float(row['Amount(INR)']) if row['DR|CR'] == 'DR' else row['Amount(INR)'], axis=1)

        elif option == "SBI Bank":
            stringio = StringIO(uploaded_file.getvalue().decode('utf-8'))
            lines = stringio.readlines()

            # Remove the specified number of lines
            lines = lines[19:len(lines)-1]

            # Write the remaining lines back to the file
            temp = tempfile.NamedTemporaryFile()
            # Open the file for writing.
            with open(temp.name, 'w') as f:
                f.writelines(lines)

            df = pd.read_csv(temp.name,delimiter='\t')
            df.columns = [col.strip() for col in df.columns]
            if 'Unnamed: 8' in df.columns:
                df = df.drop(columns=['Unnamed: 8'])
            st.write(df)
            df['Debit'] = df['Debit'].replace(' ',None)
            df['Credit'] = df['Credit'].replace(' ',None)
            df['DR|CR'] = df['Credit'].fillna(-1*df['Debit'].astype('float')).astype('float')
        elif option == "Kotak Bank":
            cols = range(6)
            df = pd.read_excel(uploaded_file, skiprows=9,usecols=cols)
            st.write(df)
            df['Amount'] = df.apply(lambda row: -1 * float(row['Amount']) if row['Dr / Cr'] == 'DR' else row['Amount'], axis=1)
        elif option == "Fincare Bank":
            df = pd.read_excel(uploaded_file, skiprows=5)
            st.write(df)
            df['Withdrawal (Dr.)'] = df['Withdrawal (Dr.)'].replace('-',None)
            df['Deposit (Cr.)'] = df['Deposit (Cr.)'].replace('-',None)
            df['DR|CR'] = df['Deposit (Cr.)'].fillna(-1*df['Withdrawal (Dr.)'].astype('float')).astype('float')

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
