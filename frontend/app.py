import streamlit as st

home_page = st.Page(
    page='views/home.py',
    title='Home',
    default=True
)

tickets_page = st.Page(
    page='views/tickets.py',
    title='Tickets'
)

projects_page = st.Page(
    page='views/projects.py',
    title='Projects'
)

users_page = st.Page(
    page='views/users.py',
    title='Users'
)

pg = st.navigation(pages=[home_page, tickets_page, projects_page, users_page])

pg.run()