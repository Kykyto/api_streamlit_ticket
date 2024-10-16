import streamlit as st
import requests

# Récupérer l'URL de l'API depuis la session state
API_BASE_URL = st.session_state.get("api_path")
PROJECTS_API_URL = f"{API_BASE_URL}/projects"


# Fonction pour récupérer les projets
def fetch_projects(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(PROJECTS_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()  # Supposons que cela retourne une liste de projets
    else:
        st.error("Échec de la récupération des projets. Veuillez réessayer plus tard.")
        return []


# Fonction pour mettre à jour un projet
def update_project(token, project_id, new_name):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"name": new_name}
    response = requests.put(f"{PROJECTS_API_URL}/{project_id}", json=payload, headers=headers)

    if response.status_code == 200:
        st.sidebar.success("Projet mis à jour avec succès !")
        return True
    else:
        st.sidebar.error("Échec de la mise à jour du projet. Veuillez réessayer.")
        return False


# Fonction pour supprimer un projet
def delete_project(token, project_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(f"{PROJECTS_API_URL}/{project_id}", headers=headers)

    if response.status_code == 200:
        st.sidebar.success("Projet supprimé avec succès !")
        return True
    elif response.status_code == 500:
        st.sidebar.error("Impossible de supprimer le projet. Veuillez d'abord supprimer les tickets associés.")
        return False
    else:
        st.sidebar.error("Échec de la suppression du projet. Veuillez réessayer.")
        return False


st.title("Projects")

if "token" in st.session_state and st.session_state["token"]:
    projects = fetch_projects(st.session_state["token"])

    if projects:
        for project in projects:
            col1, col2, col3 = st.columns([4, 1, 1], vertical_alignment="center")  # Créer des colonnes pour une mise en page agréable

            with col1:
                new_name = st.text_input("Project Name", value=project["name"],
                                         key=project["id"], label_visibility='collapsed')  # Champ pour le nouveau nom

            with col2:
                if st.button("Modifier", key=f"edit_{project['id']}"):
                    update_project(st.session_state["token"], project["id"], new_name)  # Mettre à jour le projet

            with col3:
                if st.button("Supprimer", key=f"delete_{project['id']}"):
                    delete_project(st.session_state["token"], project["id"])  # Supprimer le projet

    else:
        st.write("Aucun projet trouvé.")

    with st.expander('Create a project'):
        new_project_name = st.text_input("Project Name")
        if st.button("Create Project"):
            if new_project_name:
                headers = {
                    "Authorization": f"Bearer {st.session_state['token']}"
                }
                create_response = requests.post(PROJECTS_API_URL, json={"name": new_project_name}, headers=headers)
                if create_response.status_code == 201:
                    st.success("Projet successfully created!")
                    st.rerun()
                else:
                    st.error("Project creation failure")
            else:
                st.error("Please enter a project name")

else:
    st.warning("Please log in to see projects.")
