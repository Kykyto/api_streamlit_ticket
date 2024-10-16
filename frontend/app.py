import streamlit as st

st.session_state["api_path"] = "http://localhost:5000/api"

# Pages for the ticketing app
dashboard_page = st.Page(
    page="views/dashboard.py",
    title="Dashboard",
    icon="🏠"
)

tickets_page = st.Page(
    page="views/tickets.py",
    title="Tickets",
    icon="🎫"
)

projects_page = st.Page(
    page="views/projects.py",
    title="Projects",
    icon="📂"
)

clients_page = st.Page(
    page="views/clients.py",
    title="Clients",
    icon="👥"
)

users_page = st.Page(
    page="views/users.py",
    title="Users",
    icon="👤"
)

admin_page = st.Page(
    page="views/admin.py",
    title="Admin Panel",
    icon="🔒"
)

login_page = st.Page(
    page="views/login.py",
    title="Login",
    icon="🔑"
)

user_info = st.session_state.get("user_info")

page_list = [dashboard_page, tickets_page, projects_page, clients_page, users_page]

if user_info is None:
    page_list.append(login_page)

if user_info is not None and user_info['role'] == 'admin':
    page_list.append(admin_page)

pg = st.navigation(page_list)

with st.sidebar:
    if "token" in st.session_state and user_info is not None:
        st.write(f"Welcome {user_info['firstname']}")

        if st.button("Logout"):
            st.session_state["token"] = None
            st.session_state["user_info"] = None
            st.rerun()

pg.run()
