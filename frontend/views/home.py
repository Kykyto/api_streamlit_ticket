import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Ticketing Site", page_icon=":ticket:")

with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Home", "All Projects", "Users Management", "Login Page", "Tickets"],
        icons=["house", "folder", "person", "box-arrow-in-right", "ticket"],
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

elif selected == "All Projects":
    st.title("All Projects")
    st.write("Content for All Projects page")

elif selected == "Users Management":
    st.title("Users Management")
    st.write("Content for Users Management page")

elif selected == "Login Page":
    st.title("Login Page")
    st.write("Content for Login Page")

elif selected == "Tickets":
    st.title("Tickets")
    st.write("Content for Tickets page")
