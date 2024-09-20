import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Create directories for storing images if they don't exist
owner_photo_dir = "owner_photos"
dog_photo_dir = "dog_photos"

if not os.path.exists(owner_photo_dir):
    os.makedirs(owner_photo_dir)

if not os.path.exists(dog_photo_dir):
    os.makedirs(dog_photo_dir)

# Function to save form data to CSV
def save_to_csv(data, csv_file="lost_dog_reports.csv"):
    try:
        df = pd.DataFrame([data])
        df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
    except FileNotFoundError:
        df = pd.DataFrame([data])
        df.to_csv(csv_file, index=False)

# Function to save uploaded image
def save_uploaded_file(uploaded_file, directory, filename):
    filepath = os.path.join(directory, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath

# Streamlit UI
st.set_page_config(page_title="Lost Dog Report", page_icon="🐾", layout="centered")

st.markdown(
    """
    <style>
    .title {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: white;
        background: linear-gradient(to right, #a855f7, #ec4899);
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🐾 Lost Dog Report 🐾</div>', unsafe_allow_html=True)

# Form for user input
with st.form(key="lost_dog_report_form"):
    name = st.text_input("Your Name", placeholder="Enter your full name")
    address = st.text_area("Address", placeholder="Enter your address")
    phone = st.text_input("Phone Number", placeholder="Enter your phone number")
    email = st.text_input("Email", placeholder="Enter your email address")

    st.markdown("*Your Photo*")
    owner_photo = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"], key="owner_photo")

    st.markdown("*Dog's Photo*")
    dog_photo = st.file_uploader("Upload your dog's photo", type=["jpg", "jpeg", "png"], key="dog_photo")

    dog_name = st.text_input("Dog's Name", placeholder="Enter your dog's name")
    last_seen_info = st.text_area("Last Seen Information", placeholder="Provide details about when and where your dog was last seen")

    submit_button = st.form_submit_button(label="Submit Report")

# Background style
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom, #dbeafe, #f3e8ff);
    }
    </style>
    """,
    unsafe_allow_html=True
)

if submit_button:
    # Save text data to CSV
    form_data = {
        "Name": name,
        "Address": address,
        "Phone": phone,
        "Email": email,
        "Dog Name": dog_name,
        "Last Seen Information": last_seen_info,
        "Submission Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_to_csv(form_data)

    # Save uploaded photos
    if owner_photo:
        owner_photo_filename = f"owner_{name.replace(' ', '').lower()}{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        owner_photo_path = save_uploaded_file(owner_photo, owner_photo_dir, owner_photo_filename)
        st.success(f"Owner's photo saved at: {owner_photo_path}")

    if dog_photo:
        dog_photo_filename = f"dog_{dog_name.replace(' ', '').lower()}{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        dog_photo_path = save_uploaded_file(dog_photo, dog_photo_dir, dog_photo_filename)
        st.success(f"Dog's photo saved at: {dog_photo_path}")

    st.success("Report submitted successfully!")