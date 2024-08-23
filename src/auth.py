import os
import uuid

import boto3
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env")

COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
AWS_REGION = os.getenv("AWS_REGION")

# Cognito client configuration
client = boto3.client('cognito-idp', region_name=AWS_REGION)

def register_user(email, password, name):
    """
    Registers a new user in the AWS Cognito User Pool.

    Args:
        email (str): The user's email address, used as the username.
        password (str): The user's password.
        name (str): The user's name, an additional required attribute.

    Returns:
        dict: The response from AWS Cognito indicating success or failure.
    """
    try:
        # Generate a unique username
        unique_username = str(uuid.uuid4())
        
        response = client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=unique_username,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'name', 'Value': name}
            ]
        )
        st.success("Registration successful. Please check your email to verify your account.")
        return response
    except client.exceptions.UsernameExistsException:
        st.error("The email is already registered. Please use a different email.")
    except client.exceptions.InvalidPasswordException:
        if len(password) < 8:
            st.error("Password does not meet complexity requirements. It must be at least 8 characters long.")
        elif not any(char.isalpha() for char in password):
            st.error("Password does not meet complexity requirements. It must contain at least one letter.")
        elif not any(char.isdigit() for char in password):
            st.error("Password does not meet complexity requirements. It must contain at least one digit.")
        elif not any(char.islower() for char in password):
            st.error("Password does not meet complexity requirements. It must contain at least one lowercase letter.")
        elif not any(char.isupper() for char in password):
            st.error("Password does not meet complexity requirements. It must contain at least one uppercase letter.")
        elif not any(char in "!@#$%^&*()_+{}|:\"<>?[]" for char in password):
            st.error("Password does not meet complexity requirements. It must contain at least one special character.")
        else:
            st.error("Something went wrong. Please try again or try a different password.")

    except client.exceptions.InvalidParameterException as e:
        st.error(f"Invalid parameters: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        
def confirm_user(email, confirmation_code):
    """
    Confirms a newly registered user in the AWS Cognito User Pool.

    Args:
        email (str): The user's email address.
        confirmation_code (str): The code sent to the user's email for verification.

    Returns:
        dict: The response from AWS Cognito indicating success or failure.
    """
    try:
        response = client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=email,
            ConfirmationCode=confirmation_code
        )
        st.success("Your account has been successfully verified! You can now log in.")
        return response
    except client.exceptions.CodeMismatchException:
        st.error("The confirmation code is incorrect. Please check your email and try again.")
    except client.exceptions.ExpiredCodeException:
        st.error("The confirmation code has expired. Please request a new code.")
    except Exception as e:
        st.error(f"An error occurred during confirmation: {str(e)}")
        
def login_user(email, password):
    """
    Logs in a user by initiating the authentication flow with AWS Cognito.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        str: The access token if login is successful, otherwise None.
    """
    try:
        response = client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        access_token = response['AuthenticationResult']['AccessToken']
        st.success("Login successful!")
        return access_token
    except client.exceptions.NotAuthorizedException:
        st.error("Incorrect username or password.")
    except client.exceptions.UserNotConfirmedException:
        st.error("User is not confirmed. Please check your email for the verification link.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
