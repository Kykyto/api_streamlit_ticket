import streamlit as st
import requests

st.title("Dashboard")

# Function to fetch data (e.g., tickets, users, projects) from the API
def fetch_data(endpoint, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch {endpoint}.")
        return None

if "token" in st.session_state and st.session_state["token"]:
    st.write(f"Welcome to the dashboard, {st.session_state['user_info']['firstname']}!")

    # Example of fetching and displaying data (adjust API paths accordingly)
    tickets = fetch_data(f"{st.session_state['api_path']}/tickets", st.session_state["token"])
    users = fetch_data(f"{st.session_state['api_path']}/users", st.session_state["token"])
    projects = fetch_data(f"{st.session_state['api_path']}/projects", st.session_state["token"])

    # Display the statistics
    if tickets and users and projects:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Total Tickets")
            st.write(len(tickets))

        with col2:
            st.subheader("Total Users")
            st.write(len(users))

        with col3:
            st.subheader("Total Projects")
            st.write(len(projects))

    st.subheader("Recent Tickets")
    if tickets:
        for ticket in tickets[:5]:
            st.write(f"Ticket #{ticket['id']}: {ticket['title']}")

else:
    st.warning("Please log in to view the dashboard.")
