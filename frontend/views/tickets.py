import streamlit as st
import requests

# Récupérer l'URL de l'API depuis la session state
API_BASE_URL = st.session_state.get("api_path")
TICKETS_API_URL = f"{API_BASE_URL}/tickets"
CLIENTS_API_URL = f"{API_BASE_URL}/clients"
PROJECTS_API_URL = f"{API_BASE_URL}/projects"


def fetch_tickets(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(TICKETS_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Tickets fetch failure. Please try again later.")
        return []


def create_ticket(token, title, description, status, client_id, project_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    create_response = requests.post(TICKETS_API_URL, json={
        "title": title,
        "description": description,
        "status": status,
        "user_id": st.session_state["user_info"]["id"],
        "client_id": client_id,
        "project_id": project_id
    }, headers=headers)
    if create_response.status_code == 201:
        st.sidebar.success("Ticket created successfully!")
        return True
    else:
        st.sidebar.error("Failed to create ticket. Please try again.")
        return False


def update_ticket(token, ticket_id, title, description, status, client_id, project_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "title": title,
        "description": description,
        "status": status,
        "user_id": st.session_state["user_info"]["id"],
        "client_id": client_id,
        "project_id": project_id
    }
    response = requests.put(f"{TICKETS_API_URL}/{ticket_id}", json=payload, headers=headers)

    if response.status_code == 200:
        st.success("Ticket updated successfully!")
        return True
    else:
        st.error("Failed to update ticket. Please try again.")
        return False


def delete_ticket(token, ticket_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(f"{TICKETS_API_URL}/{ticket_id}", headers=headers)

    if response.status_code == 200:
        st.sidebar.success("Ticket deleted successfully!")
        st.rerun()
    else:
        st.sidebar.error("Failed to delete ticket. Please try again.")
        return False


@st.dialog("Ticket Info")
def ticket_info(ticket, client_name, project_name):
    st.write(f"**Title:** {ticket['title']}")
    st.write(f"**Description:** {ticket['description']}")
    st.write(f"**Status:** {ticket['status']}")
    st.write(f"**Client:** {client_name}")
    st.write(f"**Project:** {project_name}")


@st.dialog("Edit Ticket")
def edit_ticket(ticket, clients, projects):
    title = st.text_input("Title", value=ticket['title'])
    description = st.text_area("Description", value=ticket['description'])
    status = st.selectbox("Status", options=["ongoing", "paused", "complete", "cancelled"],
                          index=["ongoing", "paused", "complete", "cancelled"].index(ticket["status"]))

    client_options = {client["name"]: client["id"] for client in clients}
    project_options = {project["name"]: project["id"] for project in projects}

    client_name = st.selectbox("Client", options=list(client_options.keys()),
                               index=list(client_options.values()).index(ticket["client_id"]))
    project_name = st.selectbox("Project", options=list(project_options.keys()),
                                index=list(project_options.values()).index(ticket["project_id"]))

    if st.button("Update"):
        if update_ticket(st.session_state["token"], ticket['id'], title, description, status,
                         client_options[client_name], project_options[project_name]):
            st.rerun()


st.title("Tickets")

if "token" in st.session_state and st.session_state["token"]:
    # Fetch clients and projects for dropdowns
    clients = requests.get(CLIENTS_API_URL, headers={"Authorization": f"Bearer {st.session_state['token']}"}).json()
    projects = requests.get(PROJECTS_API_URL, headers={"Authorization": f"Bearer {st.session_state['token']}"}).json()

    tickets = fetch_tickets(st.session_state["token"])

    if tickets:
        for ticket in tickets:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])

            client_name = next(client["name"] for client in clients if client["id"] == ticket["client_id"])
            project_name = next(project["name"] for project in projects if project["id"] == ticket["project_id"])

            with col1:
                st.write(ticket['title'])

            with col2:
                st.write(ticket['status'])

            with col3:
                if st.button("All info", key=f"info_{ticket['id']}"):
                    ticket_info(ticket, client_name, project_name)

            with col4:
                if st.button("Edit", key=f"edit_{ticket['id']}"):
                    edit_ticket(ticket, clients, projects)

            with col5:
                if st.button("Delete", key=f"delete_{ticket['id']}"):
                    delete_ticket(st.session_state["token"], ticket["id"])

    # Expander to create a new ticket
    with st.expander("Create a Ticket"):
        st.subheader("Please fill the following information:")

        title = st.text_input("Title", placeholder="Enter the title")
        description = st.text_area("Description", placeholder="Enter the description")
        status = st.selectbox("Status", options=["ongoing", "paused", "complete", "cancelled"], key="create_status")

        client_options = {client["name"]: client["id"] for client in clients}
        project_options = {project["name"]: project["id"] for project in projects}

        client_name = st.selectbox("Client", options=list(client_options.keys()), key="create_client")
        project_name = st.selectbox("Project", options=list(project_options.keys()), key="create_project")

        if st.button("Create Ticket"):
            if title and description and client_options[client_name] and project_options[project_name]:
                if create_ticket(st.session_state["token"], title, description, status, client_options[client_name],
                                 project_options[project_name]):
                    st.rerun()
            else:
                st.error("Please fill out all fields.")

else:
    st.warning("Please log in to see tickets.")
