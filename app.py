import streamlit as st
import pandas as pd
from supabase import create_client
url="https://xnmzivatgiaetmhbphdz.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhubXppdmF0Z2lhZXRtaGJwaGR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk5NjE0MTMsImV4cCI6MjA5NTUzNzQxM30.FCEd471MjR1DypuK6TpMWg5dNLlhiXflh4NhHjxdB3o"
supabase=create_client(url,key)

st.sidebar.title("Navigation")
page=st.sidebar.radio("Select Page",["Student","Admin"])

if page=="Student":
    st.title("Exam Room Finder")
    roll=st.text_input("Enter Roll Number")
    if st.button("Search"):
        try:
            result=(
                supabase.table("examrooms2").select("*").eq("rollno",roll).execute()
            )
            if result.data:
                data=result.data[0]
                st.success("Exam Details Found")
                st.write(f"Room Number:{data['roomno']}")
                st.write(f"Building Name:{data['buildingname']}")
            else:
                st.error("Roll No not found")
        except Exception as e:
            st.error(f"error :{e}")
elif page=="Admin":
    st.title("Admin Upload")
    upload_file=st.file_uploader("Upload excel File",type=["xlsx"])
    if upload_file:
        df=pd.read_excel(upload_file)
        st.subheader("Preview")
        st.dataframe(df)
        if st.button("Upload Date"):
            try:
                records=df.fillna("").to_dict(orient="records")
                supbase.table("examrooms2").insert(records).execute()
                st.success(f"{len(records)} Records uploaded Successfully!")
            except Exception as e:
                st.error(f"upload failed:{e}")



