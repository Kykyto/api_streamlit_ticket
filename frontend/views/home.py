import streamlit as st
import os
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Ticketing Site", page_icon=":ticket:")
def display_user_info():
    user_info = st.session_state.get("user_info")
    if user_info:
        st.write(f"Logged in as: {user_info['username']}")
    else:
        st.write("Not logged in")

display_user_info()

st.image("frontend/views/material/working.jpg", caption="Working Image")

# Présentation du site de ticket
st.title("Bienvenue sur le site de ticketing")

st.markdown("""
Ce projet a été développé par [Jules Pichot](https://github.com/Jules-Pchot) et [Kylian Tarde](https://github.com/KylianTarde).

- **Jules Pichot** : Développeur Frontend
- **Kylian Tarde** : Développeur Backend

Le projet utilise une API et une base de données hébergées sur un serveur distant, créées par Kylian. La connexion à ce serveur est nécessaire pour accéder aux services de l'API.
""")