import streamlit as st
import requests

# Récupérer l'URL de l'API depuis la session state
API_BASE_URL = st.session_state.get("api_path")
USERS_API_URL = f"{API_BASE_URL}/users"


def fetch_users(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(USERS_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Users fetch failure. Please try again later.")
        return []


def update_user(token, user_id, firstname, name, birthdate, email, role):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "firstname": firstname,
        "name": name,
        "birthdate": birthdate,
        "email": email,
        "role": role,
        "password": ""
    }
    response = requests.put(f"{USERS_API_URL}/{user_id}", json=payload, headers=headers)

    if response.status_code == 200:
        st.success("Profile updated successfully!")
        return True
    else:
        st.error("Failed to update profile. Please try again.")
        return False


@st.dialog("User Info")
def user_info(user):
    st.write(f"First name: {user['firstname']}")
    st.write(f"Name: {user['name']}")
    st.write(f"Birthdate: {user['birthdate']}")
    st.write(f"Email: {user['email']}")
    st.write(f"Role: {user['role']}")


@st.dialog("Edit Profile")
def edit_profile(user):
    firstname = st.text_input("First name", value=user['firstname'])
    name = st.text_input("Name", value=user['name'])
    birthdate = st.text_input("Birthdate", value=user['birthdate'])
    email = st.text_input("Email", value=user['email'])
    role = st.text_input("Role", value=user['role'], disabled=True)

    if st.button("Update"):
        if update_user(st.session_state["token"], user['id'], firstname, name, birthdate, email, role):
            st.rerun()


st.title("Users")

if "token" in st.session_state and st.session_state["token"]:
    users = fetch_users(st.session_state["token"])
    current_user_id = st.session_state["user_info"]["id"]

    if users:
        for user in users:
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

            with col1:
                st.write(f"{user['firstname']}")

            with col2:
                st.write(f"{user['name']}")

            with col3:
                st.write(f"{user['email']}")

            with col4:
                if st.button("View info", key=f"info_{user['id']}"):
                    user_info(user)

            if user['id'] == current_user_id:
                with col5:
                    if st.button("Edit", key=f"edit_{user['id']}"):
                        edit_profile(user)

else:
    st.warning("Please log in to view users.")
