"""
App Script
=========

This script serves as the entry point for the DreamDX AI application. It sets up the Streamlit page configuration,
defines the title and icon, and imports the necessary modules. It also imports the functions from the `api` module for
starting, continuing, and waking up a narrative.

Usage:
-----
To run this script, execute `python app.py` in the terminal.
"""

from datetime import datetime

import streamlit as st

import components.auth as auth  # noqa: F401
from components.api import (  # noqa: F401
    continue_narrative,
    get_user_narratives,
    start_narrative,
    wake_up,
)

### --- Page Configuration --- ###

# Set up page configuration and title
st.set_page_config(
    page_title="Dream Simulator",
    page_icon="🤖​💬​"
)
st.markdown("# 🤖​💬 Dream Simulator")
st.sidebar.header("Dream Simulator")

# Check authentication
if not st.session_state.get("authenticated", False):
    auth.set_st_state_vars()

# Add login/logout button
if st.session_state.get("authenticated", False):
    auth.button_logout()
else:
    auth.button_login()
    st.stop()  # Stop execution if not authenticated

# Get user id (user email)
user_id = st.session_state.get("user_email", "")

### --- Helper Functions --- ###

def add_to_messages(role, action_type, content):
    """
    Adds an entry to the session history.

    Args:
        role (str): The role of the message ('user' or 'assistant').
        action_type (str): Indicates whether it's a 'user_action' or 'model_description'.
        content (str): The content of the action or response.
    """
    entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'role': role,
        'action_type': action_type,
        'content': content
    }

    st.session_state.messages.append(entry)


def handle_assistant_response(response_data):
    """
    Handles the response from the assistant, updating the chat and session state.

    Args:
        response_data (dict): The response from the API containing the assistant's messages.
    """
    if response_data and 'descriptions' in response_data:
        for description in response_data['descriptions']:
            with st.chat_message("assistant"):
                st.markdown(description)
            add_to_messages("assistant", "model_description", description)
    elif response_data:
        st.error("Error: 'descriptions' not found in the response from the API")


def handle_start_narrative(user_id, session_id, narrative_input):
    """
    Starts a new narrative by sending the user's input to the API
    and updating the state of the session.

    Args:
        user_id (str): The ID of the user (email).
        session_id (str): Current session identifier.
        narrative_input (str): User input to start the narrative.
    """
    response_data = start_narrative(user_id, session_id, narrative_input)
    handle_assistant_response(response_data)
    st.session_state.narrative_started = True  # Narrative started


def handle_continue_narrative(user_id, session_id, narrative_input):
    """
    Continues an existing narrative by sending the user's input to the API.

    Args:
        user_id (str): The ID of the user (email).
        session_id (str): The ID of the current session.
        narrative_input (str): The input provided by the user to continue the narrative.
    """
    response_data = continue_narrative(user_id, session_id, narrative_input)
    handle_assistant_response(response_data)


def handle_wake_up():
    """
    Ends the narrative by sending a 'wake up' command to the API and resets the session state.
    """
    response_data = wake_up()
    if response_data:
        add_to_messages('assistant', 'model_description', response_data.get('message', 'Woke up'))
    # Reset session state
    st.session_state.session_id = ""
    st.session_state.messages = []
    st.session_state.narrative_started = False
    st.rerun()


def is_valid_session_id(user_id, session_id):
    """
    Checks if the given session_id is valid (not already registered in DynamoDB).
    
    Args:
        user_id (str): The ID of the user (email).
        session_id (str): The session ID to check.
    
    Returns:
        bool: True if the session_id is valid, False otherwise.
    """
    existing_narratives = get_user_narratives(user_id)
    return not any(narrative['session_id'] == session_id for narrative in existing_narratives)

def is_existing_narrative(user_id, session_id):
    """
    Checks if the given session_id already exists for the user.
    
    Args:
        user_id (str): The ID of the user (email).
        session_id (str): The session ID to check.
    
    Returns:
        bool: True if the narrative exists, False otherwise.
    """
    existing_narratives = get_user_narratives(user_id)
    return any(narrative['session_id'] == session_id for narrative in existing_narratives)

### --- Session States Initialization --- ###

# Session identifier and access token
if 'session_id' not in st.session_state:
    st.session_state.session_id = ""

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
# Narrative started flag
if 'narrative_started' not in st.session_state:
    st.session_state.narrative_started = False  # Check if narrative is started

### --- Main App --- ###

if st.session_state.get("authenticated", False):
    # Only show the page content if the user is authenticated
    if not st.session_state.narrative_started:
        session_id = st.text_input('Dream narrative Name',
                                   placeholder='Narrative Name',
                                   value=st.session_state.session_id)
        
        # Update session_id in session state if the user changes the input
        if session_id != st.session_state.session_id:
            st.session_state.session_id = session_id
            st.session_state.narrative_started = False
        
        # Check if the session_id is valid
        if session_id:
            if is_existing_narrative(user_id, session_id):
                st.warning("Narrative already exists. Choose a new name to start a new dream.")
            else:
                st.success("You can start your dream now.")
                st.session_state.narrative_started = True
    else:
        st.write(f"**Narrative Name:** {st.session_state.session_id}")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Show chat input if a valid session_id is set and narrative is started
    if st.session_state.session_id and st.session_state.narrative_started:
        # Accept user input
        if prompt := st.chat_input("Type to dream"):
            with st.chat_message("user"):
                st.markdown(prompt)
            # Start or continue narrative as appropriate
            if len(st.session_state.messages) == 0:
                add_to_messages("user", "dream_description", prompt)
                handle_start_narrative(user_id, st.session_state.session_id, prompt)
            else:
                add_to_messages("user", "user_action", prompt)
                handle_continue_narrative(user_id, st.session_state.session_id, prompt)

        # Wake up button
        if st.button("Wake up"):
            handle_wake_up()
            # TODO: Include flow to save dream narrative if user wants to

    elif not st.session_state.session_id:
        st.write("Enter a title for your dream narrative.")
        
else:
    st.write("Please log in to use the Dream Simulator.")

#! Debug
# st.write(st.session_state)