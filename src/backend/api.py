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
        if 400 <= response.status_code < 500:
            st.error(f"Client error: {response.status_code} - {response.reason}")
        elif 500 <= response.status_code < 600:
            st.error(f"Server error: {response.status_code} - {response.reason}")
        else:
            st.error(f"Unexpected HTTP error: {response.status_code} - {http_err}")
        return None
    
    except requests.exceptions.ConnectionError:
        st.error("A connection error occurred. Please check your internet connection.")
        return None
    
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again later.")
        return None
    
    except requests.exceptions.RequestException as req_err:
        st.error(f"An unexpected error occurred: {str(req_err)}")
        return None

def start_narrative(session_id, narrative_input):
    """
    Starts a new narrative by calling the API.

    Args:
        session_id (str): The ID of the current session.
        narrative_input (str): The input provided by the user to start the narrative.

    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    endpoint = '/dev/dream/start'
    payload = {
        'command': 'start dreaming',
        'dream_description': narrative_input,
        'session_id': session_id
    }
    return call_api(endpoint, payload)

def continue_narrative(session_id, narrative_input):
    """
    Continues an existing narrative by calling the API.

    Args:
        session_id (str): The ID of the current session.
        narrative_input (str): The input provided by the user to continue the narrative.

    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    endpoint = '/dev/dream/continue'
    payload = {
        'command': 'continue narrative',
        'user_action': narrative_input,
        'session_id': session_id
    }
    return call_api(endpoint, payload)

def wake_up(session_id):
    """
    Ends the narrative by sending a 'wake up' command to the API.

    Args:
        session_id (str): The ID of the current session.

    Returns:
        dict: The JSON response from the API, or None if an error occurred.
    """
    endpoint = '/dev/dream/wake-up'
    payload = {
        'command': 'wake up',
        'session_id': session_id
    }
    return call_api(endpoint, payload)