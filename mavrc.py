import streamlit as st
import pandas as pd
import io

# Function to process the Excel file and generate the output
def process_file(uploaded_file):
    df = pd.read_excel(uploaded_file)
    output_df = df.groupby('Role_Emp_ID')['Branch ID'].apply(lambda x: ','.join(map(str, x))).reset_index()
    output_df['Length'] = output_df['Branch ID'].apply(lambda x: len(x.split(',')))
    return output_df

# Function to convert dataframe to Excel for download
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

# Streamlit app
st.title("Mavrc Mapping")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")

# Button to generate output
if uploaded_file is not None:
    if st.button("Generate Output"):
        output_df = process_file(uploaded_file)

        # Display the output dataframe in the app
        st.write("Output Data:")
        st.dataframe(output_df)

        # Convert dataframe to Excel for download
        excel_data = convert_df_to_excel(output_df)
        
        # Provide a download button for the output Excel file
        st.download_button(
            label="Download Excel File",
            data=excel_data,
            file_name="Mapping_Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
