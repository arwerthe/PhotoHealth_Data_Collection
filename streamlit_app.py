import streamlit as st
import supabase
from datetime import datetime
from supabase import create_client

# --- Supabase config (get from supabase project) ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("PhotoHealth Data Collection")
st.write("Please Enter Patient Information")

# Form
with st.form("data"):
    disease = st.text_input("Disease state")
    clinic = st.text_input("Clinic")
    age = st.number_input("Age", min_value=0, max_value=120)
    sex = st.selectbox("Sex", ["M", "F", "Other"])
    
    img1 = st.file_uploader("Image 1", type=["png","jpg","jpeg"])
    img2 = st.file_uploader("Image 2", type=["png","jpg","jpeg"])
    
    submit = st.form_submit_button("Submit")

if submit:
    if not img1 or not img2:
        st.error("Please upload two images!")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Build paths
        folder = f"{disease}/{clinic}"
        name1 = f"{folder}/{timestamp}_1_{img1.name}"
        name2 = f"{folder}/{timestamp}_2_{img2.name}"

        # Upload to Supabase
        supabase.storage.from_("Uploads").upload(name1, img1.getvalue())
        supabase.storage.from_("Uploads").upload(name2, img2.getvalue())

        st.success("Uploaded!")

        st.write("Data saved:")
        st.write(f"Disease: {disease}")
        st.write(f"Clinic: {clinic}, Age: {age}, Sex: {sex}")


