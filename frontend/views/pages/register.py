import streamlit as st
import requests

# Registration form
st.title("Register")
firstname = st.text_input("First Name")
name = st.text_input("Last Name")
birthdate = st.text_input("Birthdate (YYYY-MM-DD)")
email = st.text_input("Email")
role = st.text_input("Role")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if firstname and name and birthdate and email and role and password:
        response = requests.post("https://ticket-api-6jhy.onrender.com/api/users/", json={
            "firstname": firstname,
            "name": name,
            "birthdate": birthdate,
            "email": email,
            "role": role,
            "password": password
        })
        if response.status_code == 201:
            st.success("Registration successful!")
        else:
            st.error("Registration failed")
    else:
        st.error("Please fill out all fields")