import streamlit as st
import requests
import pandas as pd

API_BASE_URL = st.session_state.get("api_path")
USERS_API_URL = f"{API_BASE_URL}/users"


# Fetch users from the API
def fetch_users(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(USERS_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch users.")
        return []


# Update user information
def update_user(token, user_id, firstname, name, email, role, birthdate):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "firstname": firstname,
        "name": name,
        "email": email,
        "role": role,
        "birthdate": birthdate.isoformat(),  # Ensure birthdate is a string
        "password": ""
    }
    response = requests.put(f"{USERS_API_URL}/{user_id}", json=payload, headers=headers)
    if response.status_code == 200:
        st.success("User updated successfully!")
        return True
    else:
        st.error("Failed to update user.")
        return False


# Delete user
def delete_user(token, user_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(f"{USERS_API_URL}/{user_id}", headers=headers)
    if response.status_code == 200:
        st.success("User deleted successfully!")
        st.rerun()
    else:
        st.error("Failed to delete user.")


# Dialog to edit user information
@st.dialog("Edit User")
def edit_user(user):
    with st.form(key=f"edit_form_{user['id']}"):
        firstname = st.text_input("First Name", value=user['firstname'])
        name = st.text_input("Name", value=user['name'])
        email = st.text_input("Email", value=user['email'])
        role = st.selectbox("Role", options=["developer", "reporter", "admin"], index=["developer", "reporter", "admin"].index(user['role']))
        birthdate = st.date_input("Birthdate", value=pd.to_datetime(user['birthdate']).date())

        submit_button = st.form_submit_button(label="Update")
        if submit_button:
            if update_user(st.session_state["token"], user['id'], firstname, name, email, role, birthdate):
                st.rerun()


# Main dashboard
st.title("Admin Dashboard")

if "token" in st.session_state and st.session_state["token"]:
    users = fetch_users(st.session_state["token"])

    if users:
        for user in users:
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                st.write(user['firstname'])

            with col2:
                st.write(user['name'])

            with col3:
                st.write(user['email'])

            with col4:
                st.write(user['role'])

            with col5:
                if st.button("Edit", key=f"edit_{user['id']}"):
                    edit_user(user)  # Show the edit dialog

            with col6:
                if st.button("Delete", key=f"delete_{user['id']}"):
                    delete_user(st.session_state["token"], user["id"])
else:
    st.error("Please log in first.")
