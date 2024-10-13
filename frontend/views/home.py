import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Ticketing Site", page_icon=":ticket:")
def display_user_info():
    user_info = st.session_state.get("user_info")
    if user_info:
        st.write(f"Logged in as: {user_info['username']}")
    else:
        st.write("Not logged in")

display_user_info()

with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Home","Login Page", "All Projects", "Users Management", "Tickets"],
        icons=["house", "box-arrow-in-right","inbox_tray", "folder", "person", "ticket"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.title("Home Page")
    st.write("Welcome to the Ticketing Site!")
    st.header("About This Site")
    st.write("""
    This is a ticketing site where you can manage and track your tickets.
    You can create new tickets, view existing ones, and update their status.
    Use the navigation bar on the left to explore different sections of the site.
    """)

elif selected == "Login":
    import login

elif selected == "Register":
    import register

elif selected == "All Projects":
    import projects

elif selected == "Users Management":
    import users

elif selected == "Login Page":
    import login

elif selected == "Tickets":
    import tickets
