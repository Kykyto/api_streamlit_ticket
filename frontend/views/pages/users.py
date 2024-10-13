import streamlit as st
import requests
st.image("frontend/views/material/thumb.jpg")

users_response = requests.get("https://ticket-api-6jhy.onrender.com/api/users/")
clients_response = requests.get("https://ticket-api-6jhy.onrender.com/api/clients/")

if users_response.status_code == 200 and clients_response.status_code == 200:
    users = users_response.json()
    clients = clients_response.json()

    st.title("Users and Clients")

    # Display users
    st.header("Users")
    for user in users:
        st.write(f"User ID: {user['id']}, Name: {user['firstname']} {user['name']}, Email: {user['email']}, Role: {user['role']}")
        if st.button(f"Delete User {user['firstname']} {user['name']}"):
            delete_response = requests.delete(f"https://ticket-api-6jhy.onrender.com/api/users/{user['id']}")
            if delete_response.status_code == 200:
                st.success(f"User {user['firstname']} {user['name']} deleted successfully!")
            else:
                st.error(f"Failed to delete user {user['firstname']} {user['name']}")
        if st.button(f"Edit User {user['firstname']} {user['name']}"):
            new_firstname = st.text_input("New Firstname", key=f"new_firstname_{user['id']}")
            new_name = st.text_input("New Name", key=f"new_name_{user['id']}")
            new_email = st.text_input("New Email", key=f"new_email_{user['id']}")
            new_role = st.text_input("New Role", key=f"new_role_{user['id']}")
            new_password = st.text_input("New Password", key=f"new_password_{user['id']}", type="password")
            if st.button(f"Submit Edit User {user['firstname']} {user['name']}"):
                if new_firstname and new_name and new_email and new_role and new_password:
                    edit_response = requests.put(f"https://ticket-api-6jhy.onrender.com/api/users/{user['id']}", json={
                        "firstname": new_firstname,
                        "name": new_name,
                        "email": new_email,
                        "role": new_role,
                        "password": new_password
                    })
                    if edit_response.status_code == 200:
                        st.success(f"User {user['firstname']} {user['name']} updated successfully!")
                    else:
                        st.error(f"Failed to update user {user['firstname']} {user['name']}")
                else:
                    st.error("Please fill out all fields")

    # Display clients
    st.header("Clients")
    for client in clients:
        st.write(f"Client ID: {client['id']}, Name: {client['firstname']} {client['name']}, Company: {client['company']}, Email: {client['email']}, Phone: {client['phone']}")
        if st.button(f"Delete Client {client['firstname']} {client['name']}"):
            delete_response = requests.delete(f"https://ticket-api-6jhy.onrender.com/api/clients/{client['id']}")
            if delete_response.status_code == 200:
                st.success(f"Client {client['firstname']} {client['name']} deleted successfully!")
            else:
                st.error(f"Failed to delete client {client['firstname']} {client['name']}")
        if st.button(f"Edit Client {client['firstname']} {client['name']}"):
            new_firstname = st.text_input("New Firstname", key=f"new_firstname_{client['id']}")
            new_name = st.text_input("New Name", key=f"new_name_{client['id']}")
            new_company = st.text_input("New Company", key=f"new_company_{client['id']}")
            new_email = st.text_input("New Email", key=f"new_email_{client['id']}")
            new_phone = st.text_input("New Phone", key=f"new_phone_{client['id']}")
            if st.button(f"Submit Edit Client {client['firstname']} {client['name']}"):
                if new_firstname and new_name and new_company and new_email and new_phone:
                    edit_response = requests.put(f"https://ticket-api-6jhy.onrender.com/api/clients/{client['id']}", json={
                        "firstname": new_firstname,
                        "name": new_name,
                        "company": new_company,
                        "email": new_email,
                        "phone": new_phone
                    })
                    if edit_response.status_code == 200:
                        st.success(f"Client {client['firstname']} {client['name']} updated successfully!")
                    else:
                        st.error(f"Failed to update client {client['firstname']} {client['name']}")
                else:
                    st.error("Please fill out all fields")
else:
    st.error("Failed to fetch users or clients")
