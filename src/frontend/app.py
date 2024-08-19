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

from src.backend.api import continue_narrative, start_narrative, wake_up  # noqa: F401

### --- Page Configuration --- ###

# Set up page configuration and title
st.set_page_config(
    page_title="DreamDX AI",
    page_icon=":new_moon_with_face:"
)
st.title("DreamDX AI")

### --- Session States Initialization --- ###

# Session identifier
if 'session_id' not in st.session_state:
    st.session_state.session_id = ""
# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
# Narrative started flag
if 'narrative_started' not in st.session_state:
    st.session_state.narrative_started = False  # Check if narrative is started

# Only show the input field for the narrative name if the narrative hasn't started
if not st.session_state.narrative_started:
    session_id = st.text_input('Dream narrative Name',
                               placeholder='Narrative Name',
                               value=st.session_state.session_id)
    
    # Update session_id in session state if the user changes the input
    if session_id != st.session_state.session_id:
        st.session_state.session_id = session_id
else:
    st.write(f"**Narrative Name:** {st.session_state.session_id}")

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

def handle_start_narrative(session_id, narrative_input):
    """
    Starts a new narrative by sending the user's input to the API
    and updating the state of the session.

    Args:
        session_id (str): Current session identifier.
        narrative_input (str): User input to start the narrative.
    """
    response_data = start_narrative(session_id, narrative_input)
    if response_data:
        with st.chat_message("assistant"):
            st.markdown(response_data.get('description', 'Error in the response from the API'))
        add_to_messages("assistant", "model_description", response_data.get('description', 'Error in the response from the API'))
        st.session_state.narrative_started = True  # Narrative started

def handle_continue_narrative(narrative_input):
    """
    Continues an existing narrative by sending the user's input to the API.

    Args:
        narrative_input (str): The input provided by the user to continue the narrative.
    """
    response_data = continue_narrative(st.session_state.session_id, narrative_input)
    if response_data:
        with st.chat_message("assistant"):
            st.markdown(response_data.get('description', 'Error in the response from the API'))
        add_to_messages("assistant", "model_description", response_data.get('description', 'Error in the response from the API'))

def handle_wake_up():
    """
    Ends the narrative by sending a 'wake up' command to the API and resets the session state.
    """
    response_data = wake_up(st.session_state.session_id)
    if response_data:
        add_to_messages('assistant', 'model_description', response_data.get('message', 'Woke up'))
    # Reset session state
    st.session_state.session_id = ""
    st.session_state.messages = []
    st.session_state.narrative_started = False
    st.rerun()

### --- Main Logic --- ###

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Verify if session ID has been set
if st.session_state.session_id:
    # Accept user input
    if prompt := st.chat_input("Type to dream"):
        # Add user message to chat history
        
        with st.chat_message("user"):
            st.markdown(prompt)
        # Start or continue narrative as appropriate
        if not st.session_state.narrative_started:
            handle_start_narrative(st.session_state.session_id, prompt)
            add_to_messages("user", "dream_description", prompt)
        else:
            handle_continue_narrative(prompt)
            add_to_messages("user", "user_action", prompt)

    # Wake up button
    if st.button("Wake up"):
        handle_wake_up()
        # TODO: Include flow to save dream narrative if user wants to

else:
    st.write("Enter a title for your dream narrative.")


#! Debug
st.write(st.session_state)



