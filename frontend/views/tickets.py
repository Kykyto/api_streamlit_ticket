import streamlit as st
import requests

response = requests.get("https://ticket-api-6jhy.onrender.com/api/tickets/")
if response.status_code == 200:
    tickets = response.json()

    # Create new ticket form
    st.title("Create New Ticket")
    user_id = st.text_input("User ID")
    client_id = st.text_input("Client ID")
    project_id = st.text_input("Project ID")
    title = st.text_input("Title")
    description = st.text_area("Description")
    status = st.selectbox("Status", ["ongoing", "completed"])

    if st.button("Create Ticket"):
        if user_id and client_id and project_id and title and description and status:
            create_response = requests.post("https://ticket-api-6jhy.onrender.com/api/tickets/", json={
                "user_id": user_id,
                "client_id": client_id,
                "project_id": project_id,
                "title": title,
                "description": description,
                "status": status
            })
            if create_response.status_code == 201:
                st.success("Ticket created successfully!")
            else:
                st.error("Failed to create ticket")
        else:
            st.error("Please fill out all fields")

    # Display existing tickets
    st.title("Existing Tickets")
    for ticket in tickets:
        st.write(f"Ticket ID: {ticket['id']}, Title: {ticket['title']}, Description: {ticket['description']}, Status: {ticket['status']}")

        if st.button(f"Delete {ticket['title']}"):
            delete_response = requests.delete(f"https://ticket-api-6jhy.onrender.com/api/tickets/{ticket['id']}")
            if delete_response.status_code == 200:
                st.success(f"Ticket {ticket['title']} deleted successfully!")
            else:
                st.error(f"Failed to delete ticket {ticket['title']}")

        if st.button(f"Edit {ticket['title']}"):
            new_title = st.text_input("New Title", key=f"new_title_{ticket['id']}")
            new_description = st.text_area("New Description", key=f"new_description_{ticket['id']}")
            new_status = st.selectbox("New Status", ["ongoing", "completed"], key=f"new_status_{ticket['id']}")

            if st.button(f"Submit Edit {ticket['title']}"):
                if new_title and new_description and new_status:
                    edit_response = requests.put(f"https://ticket-api-6jhy.onrender.com/api/tickets/{ticket['id']}", json={
                        "user_id": ticket['user_id'],
                        "client_id": ticket['client_id'],
                        "project_id": ticket['project_id'],
                        "title": new_title,
                        "description": new_description,
                        "status": new_status
                    })
                    if edit_response.status_code == 200:
                        st.success(f"Ticket {ticket['title']} updated successfully!")
                    else:
                        st.error(f"Failed to update ticket {ticket['title']}")
                else:
                    st.error("Please fill out all fields")
else:
    st.error("Failed to fetch tickets")