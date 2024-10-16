import streamlit as st
import requests


# Récupérer l'URL de l'API depuis la session state
API_BASE_URL = st.session_state.get("api_path")
CLIENTS_API_URL = f"{API_BASE_URL}/clients"


def fetch_clients(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(CLIENTS_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Clients fetch failure. Please try again later.")
        return []


def create_client(token, firstname, name, company, email, phone):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    create_response = requests.post(CLIENTS_API_URL, json={
        "firstname": firstname,
        "name": name,
        "company": company,
        "email": email,
        "phone": phone
    }, headers=headers)
    if create_response.status_code == 201:
        st.sidebar.success("Client created successfully!")
        return True
    else:
        st.sidebar.error("Failed to create client. Please try again.")
        return False


def update_client(token, client_id, firstname, name, company, email, phone):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "firstname": firstname,
        "name": name,
        "company": company,
        "email": email,
        "phone": phone
    }
    response = requests.put(f"{CLIENTS_API_URL}/{client_id}", json=payload, headers=headers)

    if response.status_code == 200:
        st.success("Client updated successfully!")
        return True
    else:
        st.error("Failed to update client. Please try again.")
        return False


def delete_client(token, client_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(f"{CLIENTS_API_URL}/{client_id}", headers=headers)

    if response.status_code == 200:
        st.sidebar.success("Client deleted successfully!")
        st.rerun()
    elif response.status_code == 500:
        st.sidebar.error("Failed to delete client. Client may be linked to a ticket.")
        return False
    else:
        st.sidebar.error("Failed to delete client. Please try again.")
        return False


@st.dialog("Client Info")
def client_info(client):
    st.write(f"First name: {client['firstname']}")
    st.write(f"Name: {client['name']}")
    st.write(f"Company: {client['company']}")
    st.write(f"Email: {client['email']}")
    st.write(f"Phone: {client['phone']}")


@st.dialog("Edit Client")
def edit_client(client):
    firstname = st.text_input("First name", value=client['firstname'])
    name = st.text_input("Name", value=client['name'])
    company = st.text_input("Company", value=client['company'])
    email = st.text_input("Email", value=client['email'])
    phone = st.text_input("Phone", value=client['phone'])

    if st.button("Update"):
        if update_client(st.session_state["token"], client['id'], firstname, name, company, email, phone):
            st.rerun()


st.title("Clients")

if "token" in st.session_state and st.session_state["token"]:
    clients = fetch_clients(st.session_state["token"])

    if clients:
        for client in clients:
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

            with col1:
                st.write(f"{client['firstname']}")

            with col2:
                st.write(f"{client['name']}")

            with col3:
                st.write(f"{client['company']}")

            with col4:
                if st.button("All info", key=f"info_{client['id']}"):
                    client_info(client)

            with col5:
                if st.button("Edit", key=f"edit_{client['id']}"):
                    edit_client(client)

            with col6:
                if st.button("Delete", key=f"delete_{client['id']}"):
                    delete_client(st.session_state["token"], client["id"])

    with st.expander("Create a client"):
        # Formulaire de création de client
        st.subheader("Please fill the following informations :")

        # Champs du formulaire
        prenom = st.text_input("First name", placeholder="Enter the first name")
        nom = st.text_input("Name", placeholder="Enter the name")
        entreprise = st.text_input("Company", placeholder="Enter company name")
        email = st.text_input("Email", placeholder="Enter email address")
        telephone = st.text_input("Phone number", placeholder="Enter phone number")

        # Bouton pour soumettre le formulaire
        if st.button("Create client"):
            if prenom and nom and entreprise and email and telephone:
                if create_client(st.session_state["token"], prenom, nom, entreprise, email, telephone):
                    st.rerun()
            else:
                st.error("Please fill out all fields")

else:
    st.warning("Please log in to see clients.")
