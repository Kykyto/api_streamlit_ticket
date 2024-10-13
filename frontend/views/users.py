import streamlit as st

import requests

# Fetch users
response = requests.get("http://localhost:5000/api/users/")
if response.status_code == 200:
    users = response.json()
    for user in users:
        st.write(f"User ID: {user['id']}, Username: {user['username']}")
        if st.button(f"Delete {user['username']}"):
            delete_response = requests.delete(f"http://localhost:5000/api/users/{user['id']}")
            if delete_response.status_code == 200:
                st.success(f"User {user['username']} deleted successfully!")
            else:
                st.error(f"Failed to delete user {user['username']}")
        if st.button(f"Edit {user['username']}"):
            st.text_input("New Username", key=f"new_username_{user['id']}")
            if st.button(f"Submit Edit {user['username']}"):
                new_username = st.session_state.get(f"new_username_{user['id']}")
                if new_username:
                    edit_response = requests.put(f"http://localhost:5000/api/users/{user['id']}", data={"username": new_username})
                    if edit_response.status_code == 200:
                        st.success(f"User {user['username']} updated successfully!")
                    else:
                        st.error(f"Failed to update user {user['username']}")
                else:
                    st.error("Please enter a new username")
else:
    st.error("Failed to fetch users")
