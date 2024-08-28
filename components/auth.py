"""
Auth Script
==========

This script contains functions for handling the authentication process in the DreamDX AI application.

The script uses AWS Cognito for user authentication and session management. It includes functions for
setting up the Streamlit page configuration, defining the title and icon, and importing the necessary modules. It also includes
functions for handling authentication and API calls.

Refereces:
----------
- https://github.com/MausamGaurav/Streamlit_Multipage_AWSCognito_User_Authentication_Authorization
- https://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
"""

import base64 # noqa
import json # noqa
import os

import requests # noqa
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="config/.env")
COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
APP_URI = os.environ.get("APP_URI")

def initialise_st_state_vars():
    """
    Initializes the session state variables.
    """
    if "auth_code" not in st.session_state:
        st.session_state["auth_code"] = ""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    

def get_auth_code():
    """
    Gets the authorization code from the URL query parameters.

    Returns:
        auth_code (str): The authorization code, or an empty string if not found.
    """
    auth_query_params = st.query_params
    try:
        auth_code = auth_query_params["code"]
    except (KeyError, TypeError):
        auth_code = ""

    return auth_code
    
    
def get_user_token(auth_code):
    """
    Gets the user token from the authorization code by making a POST request call.
    
    Args:
        auth_code (str): The authorization code obtained from cognito server.
    
    Returns:
        {
        access_token (str): The access token, or an empty string if not found.
        id_token (str): The id token, or an empty string if not found.
        }
    """
    # Variables to be used in the POST request
    token_url = f"{COGNITO_DOMAIN}/oauth2/token"
    client_secret_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_secret_encoded = str(
        base64.b64encode(client_secret_string.encode("utf-8")), "utf-8")
    auth_header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {client_secret_encoded}"
        }
    auth_body = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": auth_code,
        "redirect_uri": APP_URI
    }
    # Send POST request
    token_response = requests.post(token_url,
                                   headers=auth_header, data=auth_body)

    if token_response.status_code != 200:
        access_token = ""
        id_token = ""
        return access_token, id_token
    
    try:
        access_token = token_response.json()["access_token"]
        id_token = token_response.json()["id_token"]
    except (KeyError, TypeError):
        access_token = ""
        id_token = ""
    return access_token, id_token
    
    
def pad_base64(data):
    """
    Pads the base64 string.

    Args:
        data (str): The base64 string to pad.

    Returns:
        str: The padded base64 string.  
    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += "=" * (4 - missing_padding)
    return data


def set_st_state_vars():
    """
    Sets the session state variables after authentication.
    """
    initialise_st_state_vars()
    auth_code = get_auth_code()
    access_token, id_token = get_user_token(auth_code)
    
    if access_token != "":
        st.session_state["auth_code"] = auth_code
        st.session_state["authenticated"] = True


### --- Login/logout components --- ###

login_link = f"{COGNITO_DOMAIN}/login?client_id={CLIENT_ID}&response_type=code&scope=email+openid&redirect_uri={APP_URI}"
logout_link = f"{COGNITO_DOMAIN}/logout?client_id={CLIENT_ID}&logout_uri={APP_URI}"

html_css_login = """
<style>
.button-login {
  background-color: skyblue;
  color: white !important;
  padding: 1em 1.5em;
  text-decoration: none;
  text-transform: uppercase;
}

.button-login:hover {
  background-color: #555;
  text-decoration: none;
}

.button-login:active {
  background-color: black;
}

</style>
"""

html_button_login = (
    html_css_login
    + f"<a href='{login_link}' class='button-login' target='_self'>Log In</a>"
)
html_button_logout = (
    html_css_login
    + f"<a href='{logout_link}' class='button-login' target='_self'>Log Out</a>"
)


def button_login():
    """
    Returns:
        Html of the login button.
    """
    return st.sidebar.markdown(f"{html_button_login}", unsafe_allow_html=True)


def button_logout():
    """

    Returns:
        Html of the logout button.
    """
    return st.sidebar.markdown(f"{html_button_logout}", unsafe_allow_html=True)