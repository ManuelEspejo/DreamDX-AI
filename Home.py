import streamlit as st

import components.auth as auth

st.set_page_config(
    page_title="DreamDX",
    page_icon=":new_moon_with_face:"
)
st.write("# Welcome to DreamDX AI! :night_with_stars:")
st.markdown(
    """
    DreamDX AI is an AI-powered application that allows you to revisit and take control of your dreams.

    ### Documentation
    - Github repo: [DreamDX AI](https://github.com/ManuelEspejo/DreamDX-AI)
"""
)

# Check authentication
auth.set_st_state_vars()

# Login/logout button
if st.session_state["authenticated"]:
    auth.button_logout()
else:
    auth.button_login()