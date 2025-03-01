import streamlit as st
import pandas as pd 
import os 
from io import BytesIo 

st.set_page_config(page_titel="Data sweeper" ,layout='wide') 

#custom css
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
        }    
        </style>   
        """,
        unsafe_allow_html=True
)

#titel and dedscription
st.title("Data sweeper sterling Intergator By Ainy Azhar")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning")

# file uploader
uploaded_files = st.file_uploader("upload your files (acceppts CSV or Excel):", type=["CSV","xlsx"], accept_multiple_files=(true))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv": 
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsuported file type: {file_ext}")
            continue

#file detail
st.write(" preview the head of the Dataframe")
st.dataframe(df.head())

# data cleaning options
st. subheader("Data cleaning options") 
if st.checkbox(f"Clean data for {file.name}"):
    col1, col2 = st.colums(2)

    with col1:
        if st.button(f"Remove duplicates from the file : {file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("Duplicates removed!")
 
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(includes=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        st.subheader("Select columns to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns) 



#data visualization
        st.subheader("Data visualization")
        if st.checkbox(f"show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2]) 


#Conversion options
        st.subheader("conversion options")
        conversion_type = st.radio(f"convert {file.name} to:", ["CVS" , "Excel"], key=file.nmae) 
        if st.button(f"convert{file.name}"):
            buffer = BytesIo()
            if conversion_type == "CSV":
                df.to.csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mine_type = "text/csv"

            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.shwwt"
                buffer.seek(0)

                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
st.success("All files processed successfully!")
