import streamlit as st
import requests
from streamlit_option_menu import option_menu

# Login form
st.title("Login")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if email and password:
        response = requests.post("http://localhost:5000/api/auth/", data={"email": email, "password": password})
        if response.status_code == 200:
            st.success("Login successful!")
            token = response.json().get("access_token")
            st.session_state["token"] = token
        else:
            st.error("Invalid credentials")
    else:
        st.error("Please enter both email and password")


