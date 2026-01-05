import streamlit as st
import supabase
from PIL import Image
import io
from datetime import datetime
from supabase import create_client

# --- Supabase config ---
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
    if not img1 or not img2 or not disease or not clinic:
        st.error("Please fill all fields and upload 2 images!")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = f"{disease}/{clinic}"
        # Process and upload images
        for i, img in enumerate([img1, img2], 1):
            # Open, convert to RGB, resize
            image = Image.open(img).convert("RGB").resize((224, 224))
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="JPEG")
            img_bytes = img_bytes.getvalue()

            #Build path
            name = f"{folder}/{timestamp}_img{i}.jpg"
            try:
                supabase.storage.from_("uploads").upload(name, img_bytes)
            except Exception as e:
                st.error(f"Failed to upload image {i}: {e}")
                continue

        st.success("Uploaded!")

        st.write("Data saved:")
        st.write(f"Disease: {disease}")
        st.write(f"Clinic: {clinic}, Age: {age}, Sex: {sex}")


