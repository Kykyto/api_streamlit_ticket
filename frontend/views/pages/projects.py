import streamlit as st
import requests
st.image("frontend/views/material/woah.jpg")

# Fetch projects
response = requests.get("https://ticket-api-6jhy.onrender.com/api/projects/")
if response.status_code == 200:
    projects = response.json()
    st.title("Projects")

    # Create new project form
    st.header("Create New Project")
    new_project_name = st.text_input("New Project Name")
    if st.button("Create Project"):
        if new_project_name:
            create_response = requests.post("https://ticket-api-6jhy.onrender.com/api/projects/", json={"name": new_project_name})
            if create_response.status_code == 201:
                st.success("Project created successfully!")
            else:
                st.error("Failed to create project")
        else:
            st.error("Please enter a project name")

    # Display existing projects
    st.header("Existing Projects")
    for project in projects:
        st.write(f"Project ID: {project['id']}, Project Name: {project['name']}")
        if st.button(f"Delete {project['name']}"):
            delete_response = requests.delete(f"https://ticket-api-6jhy.onrender.com/api/projects/{project['id']}")
            if delete_response.status_code == 200:
                st.success(f"Project {project['name']} deleted successfully!")
            else:
                st.error(f"Failed to delete project {project['name']}")
        if st.button(f"Edit {project['name']}"):
            new_name = st.text_input("New Project Name", key=f"new_name_{project['id']}")
            if st.button(f"Submit Edit {project['name']}"):
                if new_name:
                    edit_response = requests.put(f"https://ticket-api-6jhy.onrender.com/api/projects/{project['id']}", json={"name": new_name})
                    if edit_response.status_code == 200:
                        st.success(f"Project {project['name']} updated successfully!")
                    else:
                        st.error(f"Failed to update project {project['name']}")
                else:
                    st.error("Please enter a new name")
else:
    st.error("Failed to fetch projects")