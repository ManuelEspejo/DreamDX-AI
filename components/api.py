"""
API Script
==========

This script contains the main functions for making API calls to the DreamDX AI.
"""

import os

import requests
import streamlit as st
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

load_dotenv(dotenv_path="config/.env")

# Load the API base URL from environment variables
API_BASE_URL = os.getenv("API_BASE_URL")

# Validate that the API_BASE_URL is set
if not API_BASE_URL:
    st.error("API_BASE_URL is not set. Please check your environment configuration.")
    st.stop()

def call_api(endpoint, payload, max_retries=3, backoff_factor=0.3):
    """
    Helper function to call the API and handle errors with retries.
    
    Args:
        endpoint (str): The relative API endpoint to call (e.g., "/dev/dream/start").
        payload (dict): The payload to send with the request.
        max_retries (int): The maximum number of retry attempts.
        backoff_factor (float): A backoff factor to apply between attempts.

    Returns:
        dict or None: The JSON response from the API, or None if an error occurred.
    """
    # Create a session
    session = requests.Session()
    
    # Set up retries
    retries = Retry(total=max_retries, backoff_factor=backoff_factor, 
                    status_forcelist=[500, 502, 503, 504])
    
    # Mount it for HTTPAdapter
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    
    # Complete URL with base URL
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        # Send the POST request to the API endpoint
        response = session.post(url, json=payload)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx, 5xx)
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors
        error_message = f"HTTP error occurred: {http_err}"
        st.error(error_message)
        st.error(f"Status code: {response.status_code}")
        st.error(f"Response content: {response.text}")
        
        # Log additional request details
        st.error(f"Request URL: {url}")
        st.error(f"Request payload: {payload}")
        st.error(f"Request headers: {response.request.headers}")
        
        return None
    
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"Connection error occurred: {conn_err}")
        return None
    
    except requests.exceptions.Timeout as timeout_err:
        st.error(f"Request timed out: {timeout_err}")
        return None
    
    except requests.exceptions.RequestException as req_err:
        st.error(f"An unexpected error occurred: {req_err}")
        return None

def start_narrative(user_id, session_id, narrative_input):
    """
    Starts a new narrative by calling the API.

    Args:
        user_id (str): The ID of the user (email).
        session_id (str): The ID of the current session.
        narrative_input (str): The input provided by the user to start the narrative.

    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    endpoint = '/dev/dream/start'
    payload = {
        'command': 'start dreaming',
        'dream_description': narrative_input,
        'session_id': session_id,
        'user_id': user_id
    }
    return call_api(endpoint, payload)

def continue_narrative(user_id, session_id, narrative_input):
    """
    Continues an existing narrative by calling the API.

    Args:
        user_id (str): The ID of the user (email).
        session_id (str): The ID of the current session.
        narrative_input (str): The input provided by the user to continue the narrative.

    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    endpoint = '/dev/dream/continue'
    payload = {
        'command': 'continue narrative',
        'user_action': narrative_input,
        'session_id': session_id,
        'user_id': user_id
    }
    return call_api(endpoint, payload)

def wake_up():
    """
    Ends the current dream session by sending a 'wake up' command to the API.
    
    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    endpoint = '/dev/dream/wake-up'
    payload = {
        'command': 'wake up',
    }
    return call_api(endpoint, payload)

def get_user_narratives(user_id):
    """
    Retrieves the narratives for a given user.

    Args:
        user_id (str): The ID of the user (email).

    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    endpoint = '/dev/narratives/get-narratives'
    payload = {
        'command': 'get narratives',
        'user_id': user_id
    }
    return call_api(endpoint, payload)

def delete_narrative(user_id, session_id):
    """ 
    Deletes a narrative for a given user.

    Args:
        user_id (str): The ID of the user (email).
        session_id (str): The ID of the current session.

    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    endpoint = '/dev/narratives/delete'
    payload = {
        'command': 'delete narrative',
        'session_id': session_id,
        'user_id': user_id
    }
    return call_api(endpoint, payload)

def get_narrative_content(user_id, session_id):
    """
    Retrieves the content of a specific narrative.

    Args:
        user_id (str): The ID of the user (email).
        session_id (str): The ID of the narrative session.

    Returns:
        dict: The narrative content including prompts and descriptions.
    """
    endpoint = "/dev/narratives/get-content"
    payload = {
        "command": "get narrative content",
        "user_id": user_id,
        "session_id": session_id
    }
    
    return call_api(endpoint, payload)