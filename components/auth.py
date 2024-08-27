import base64 # noqa
import json # noqa
import os

import requests # noqa
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
APP_URI = os.environ.get("APP_URI")



def get_auth_code():
    """
    Gets the authorization code from the URL query parameters.

    Returns:
        str: The authorization code, or an empty string if not found.
    """
    auth_query_params = st.query_params()
    try:
        auth_code = auth_query_params["code"][0]
    except (KeyError, TypeError):
        auth_code = ""

    return auth_code
    
    
