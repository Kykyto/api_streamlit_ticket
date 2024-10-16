import streamlit as st
import requests


# Function to login and get user info (token and role)
def login(email, password):
    login_data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/api/auth", json=login_data)

    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        user_info = data.get("user_info")  # Contains id, email, and role

        # Store token and user info in session_state
        st.session_state["token"] = token
        st.session_state["user_info"] = user_info
        return True
    else:
        st.error("Invalid credentials")
        return False


# Function to register a new user
def register(firstname, name, birthdate, role, email, password):
    register_data = {
        "firstname": firstname,
        "name": name,
        "birthdate": birthdate,
        "role": role,
        "email": email,
        "password": password
    }
    response = requests.post("http://localhost:5000/api/users", json=register_data)

    if response.status_code == 201:
        st.success("Account created successfully! You can log in.")
        return True
    else:
        st.error("Failed to create account. Please try again.")
        return False


if "token" in st.session_state and st.session_state['user_info'] is not None:
    st.info("You are already logged in.")
else:
    # Check if the user wants to log in or register
    if "account_mode" not in st.session_state:
        st.session_state["account_mode"] = "login"  # Default mode is login

    # Toggle between login and register
    if st.session_state["account_mode"] == "login":
        st.title("Login")

        # Input fields for email and password
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Login"):
            if login(email, password):
                first_name = st.session_state["user_info"].get("firstname")
                st.success(f"Login successful, welcome {first_name}!")
                st.rerun()  # Rerun the app to show the dashboard

        st.write("Don't have an account?")
        if st.button("Create an account"):
            st.session_state["account_mode"] = "register"
            st.rerun()

    elif st.session_state["account_mode"] == "register":
        st.title("Create an account")

        # Input fields for registration
        firstname = st.text_input("First Name", placeholder="Enter your first name")
        name = st.text_input("Name", placeholder="Enter your name")
        birthdate = st.date_input("Birthdate")  # Date input for birthdate
        role = st.radio("Role", options=["developer", "reporter"], horizontal=True)  # Toggle using radio buttons
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Register"):
            # Format birthdate to string (e.g., 'YYYY-MM-DD')
            birthdate_str = birthdate.strftime('%Y-%m-%d')

            if register(firstname, name, birthdate_str, role, email, password):
                st.session_state["account_mode"] = "login"

        if st.button("Already have an account? Log in"):
            st.session_state["account_mode"] = "login"
            st.rerun()
