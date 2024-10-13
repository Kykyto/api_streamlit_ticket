import streamlit as st
import requests

response = requests.get("http://localhost:5000/api/tickets/")
if response.status_code == 200:
    tickets = response.json()
    for ticket in tickets:
        st.write(f"Ticket ID: {ticket['id']}, Ticket Title: {ticket['title']}")
        if st.button(f"Delete {ticket['title']}"):
            delete_response = requests.delete(f"http://localhost:5000/api/tickets/{ticket['id']}")
            if delete_response.status_code == 200:
                st.success(f"Ticket {ticket['title']} deleted successfully!")
            else:
                st.error(f"Failed to delete ticket {ticket['title']}")
        if st.button(f"Edit {ticket['title']}"):
            st.text_input("New Ticket Title", key=f"new_title_{ticket['id']}")
            if st.button(f"Submit Edit {ticket['title']}"):
                new_title = st.session_state.get(f"new_title_{ticket['id']}")
                if new_title:
                    edit_response = requests.put(f"http://localhost:5000/api/tickets/{ticket['id']}", data={"title": new_title})
                    if edit_response.status_code == 200:
                        st.success(f"Ticket {ticket['title']} updated successfully!")
                    else:
                        st.error(f"Failed to update ticket {ticket['title']}")
                else:
                    st.error("Please enter a new title")
else:
    st.error("Failed to fetch tickets")