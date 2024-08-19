"""
Dream Handler Script
====================

This script contains the main function for handling dreams. It includes functions for starting a new narrative, continuing
an existing narrative, and waking up from a dream. 

The script uses the OpenAI GPT-4o-mini model to generate descriptive environments and continue narratives based on user input.
The generated narratives are stored in DynamoDB for later retrieval.

"""

import json
import time

import boto3
from boto3.dynamodb.conditions import Key
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Define prompt templates for generating and continuing narratives
INITIAL_PROMPT_TEMPLATE = """
Based on the following context, generate a descriptive environment for the beginning of a narrative:
{context}

Remember:
- Address the reader directly as the protagonist, making them feel like they're experiencing it firsthand.
- Use simple, conversational language, as if narrating a dream to a friend.
- Keep the story concise, use no more than 100 words.
---

Description:
"""

CONTINUATION_PROMPT_TEMPLATE = """
Continue the narrative focusing on the immediate next action and the current scene.
- Keep the narrative short but informative about the scene, no more than 100 words.
- Avoid using concluding phrases or wrapping up the story
- Be creative and imaginative. Feel free to introduce new elements and unexpected twists
- Avoid controlling the user actions, just control the setup or character.
- Introduce new elements and unexpected twists to make the narrative more engaging.
"""

# Initialize the language model once for efficiency
model = ChatOpenAI(model="gpt-4o-mini")

# Set up DynamoDB resource and table reference for storing narratives
dynamodb = boto3.resource('dynamodb')
narrative_table = dynamodb.Table('narrative-table')  # Replace with actual table name


def start_narrative(session_id, context):
    """
    Initiates a new narrative session in DynamoDB.

    - Generates a descriptive environment based on the provided context.
    - Stores the generated narrative in DynamoDB with the session ID and a timestamp.
    
    Args:
    session_id (str): Unique identifier for the session.
    context (str): Context to seed the narrative generation.

    Returns:
    dict: The stored narrative item including session ID, timestamp, prompt, and description.
    """
    timestamp = int(time.time())  # Current timestamp for record keeping

    # Create and format the prompt using the initial template
    prompt_template = ChatPromptTemplate.from_template(INITIAL_PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context)
    description = model.invoke(prompt).content.strip()

    # Prepare the item to be stored in the database
    item = {
        'session-id': session_id,
        'timestamp': timestamp,
        'prompt': prompt,
        'description': f"You open your eyes, this is the first thing that you see...\n\n{description}\n",
        'actions': []
    }
    narrative_table.put_item(Item=item)  # Save the item in DynamoDB
    return item


def continue_narrative(session_id, user_action):
    """
    Continues an existing narrative session by extending the story.

    - Retrieves the latest narrative entry from DynamoDB.
    - Appends the user's action to the narrative and generates the next segment.
    - Stores the updated narrative in DynamoDB with the session ID and a new timestamp.
    
    Args:
    session_id (str): Unique identifier for the session.
    user_action (str): The user's input or action to continue the narrative.

    Returns:
    dict: The updated narrative item including session ID, timestamp, prompt, and description.
    """
    response = narrative_table.query(
        KeyConditionExpression=Key('session-id').eq(session_id)
    )
    
    # Handle case where the session is not found
    if 'Items' not in response or not response['Items']:
        return {"error": "Session not found."}

    # Get the most recent narrative entry
    latest_item = max(response['Items'], key=lambda x: x['timestamp'])
    previous_descriptions = " ".join([item['description'] for item in response['Items']])

    # Create a new prompt with the latest user action and previous narrative
    new_prompt = f"{previous_descriptions}\nUser action: {user_action}\n\n{CONTINUATION_PROMPT_TEMPLATE}"
    response_text = model.invoke(new_prompt).content.strip()
    
    # Prepare the new item to update in the database
    timestamp = int(time.time())
    new_item = {
        'session-id': session_id,
        'timestamp': timestamp,
        'prompt': new_prompt,
        'description': response_text,
        'actions': latest_item.get('actions', []) + [user_action]
    }
    narrative_table.put_item(Item=new_item)  # Update the item in DynamoDB
    return new_item


def delete_narrative(session_id):
    """
    Placeholder function for deleting a narrative session.
    
    Currently not implemented.
    
    Args:
    session_id (str): Unique identifier for the session.
    """
    # TODO: Implement deletion logic



def lambda_handler(event, context):
    """
    Handles incoming Lambda events and routes commands to appropriate functions.

    - Supports 'start dreaming', 'continue narrative', and 'wake up' commands.
    - Extracts command and parameters from the event and processes them accordingly.
    
    Args:
    event (dict): The incoming event containing command and parameters.
    context (dict): The context in which the event is executed.

    Returns:
    dict: The response object including status code and body.
    """
    print(f"EVENT_CONTENT: {event}")  # Debug log to check event structure

    # Determine if the event was invoked directly or via API Gateway
    if 'body' in event:
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            body = {}
    else:
        body = event  # Direct invocation without API Gateway

    # Extract relevant information from the event body
    command = body.get('command', '').lower()
    dream_description = body.get('dream_description')
    user_action = body.get('user_action')
    session_id = body.get('session_id', 'default_session')  # Replace with actual session management logic

    print(f"SESSION_ID: {session_id}")  # Debug log to trace session ID

    # Route the command to the appropriate function
    result = {}
    if command == "start dreaming" and dream_description:
        result = start_narrative(session_id, dream_description)
    elif command == "continue narrative" and user_action:
        result = continue_narrative(session_id, user_action)
    elif command == "wake up":
        result = {"message": "You woke up."}
    else:
        result = {"error": "Unknown command or missing arguments. Please use 'start dreaming' or 'continue narrative'."}

    # Return the result as a JSON response
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
