import streamlit as st
import requests

# Fetch projects
response = requests.get("http://localhost:5000/api/projects/")
if response.status_code == 200:
    projects = response.json()
    for project in projects:
        st.write(f"Project ID: {project['id']}, Project Name: {project['name']}")
else:
    st.error("Failed to fetch projects")

for project in response:
    st.write(f"Project ID: {project['id']}, Project Name: {project['name']}")
    if st.button(f"Delete {project['name']}"):
        delete_response = requests.delete(f"http://localhost:5000/api/projects/{project['id']}")
        if delete_response.status_code == 200:
            st.success(f"Project {project['name']} deleted successfully!")
        else:
            st.error(f"Failed to delete project {project['name']}")
    if st.button(f"Edit {project['name']}"):
        st.text_input("New Project Name", key=f"new_name_{project['id']}")
        if st.button(f"Submit Edit {project['name']}"):
            new_name = st.session_state.get(f"new_name_{project['id']}")
            if new_name:
                edit_response = requests.put(f"http://localhost:5000/api/projects/{project['id']}", data={"name": new_name})
                if edit_response.status_code == 200:
                    st.success(f"Project {project['name']} updated successfully!")
                else:
                    st.error(f"Failed to update project {project['name']}")
            else:
                st.error("Please enter a new name")
else:
    st.error("Failed to fetch projects")