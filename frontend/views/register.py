import streamlit as st
import requests
# Registration form
st.title("Register")
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if username and email and password:
        response = requests.post("http://localhost:5000/api/register/", data={"username": username, "email": email, "password": password})
        if response.status_code == 201:
            st.success("Registration successful!")
        else:
            st.error("Registration failed")
    else:
        st.error("Please fill out all fields")