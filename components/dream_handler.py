"""
Dream Handler Script
====================

This script contains the main functions for handling dreams and managing dream narratives.
It includes functions for starting a new narrative, continuing an existing narrative,
waking up from a dream, and retrieving user narratives.

The script uses the OpenAI GPT-4o-mini model to generate descriptive environments and
continue narratives based on user input. The generated narratives are stored in DynamoDB
for later retrieval.

"""

import json
import time
from datetime import datetime
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr, Key
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
narrative_table = dynamodb.Table('dreamdx-narratives')  # Replace with actual table name

def decimal_default(obj):
    """
    Custom JSON encoder to handle Decimal objects.
    
    Necessary because DynamoDB returns Decimal objects
    that cannot be directly serialized by json.dumps
    """
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def start_narrative(user_id, session_id, context):
    """
    Initiates a new narrative session in DynamoDB.

    - Checks if a narrative already exists for the given session ID.
    - If it doesn't exist, generates a descriptive environment and stores it.
    - If it exists, returns a warning message.
    
    Args:
    user_id (str): Unique identifier for the user (user email).
    session_id (str): Unique identifier for the session.
    context (str): Context to seed the narrative generation.

    Returns:
    dict: The stored narrative item or a warning message.
    """
    # Check if a narrative already exists for the given session ID
    existing_session = narrative_table.get_item(
        Key={'user_id': user_id, 'session_id': session_id}
        ).get('Item')
    
    if existing_session:
        return {
            "error": "Narrative already exists for the given session ID. Please use a new dream name."
            }
    timestamp = int(time.time())  # Current timestamp for record keeping
    date = datetime.now().strftime("%Y-%m-%d")

    # Create and format the prompt using the initial template
    prompt_template = ChatPromptTemplate.from_template(INITIAL_PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context)
    description = model.invoke(prompt).content.strip()

    # Prepare the item to be stored in the database
    item = {
        'user_id': user_id,
        'session_id': session_id,
        'timestamp': timestamp,
        'date': date,
        'prompt': prompt,
        'description': f"You open your eyes, this is the first thing that you see...\n\n{description}\n",
        'actions': [],
        'is_deleted': False
    }
    narrative_table.put_item(Item=item)  # Save the item in DynamoDB
    return item


def continue_narrative(user_id, session_id, user_action):
    """
    Continues an existing narrative session by extending the story.

    - Retrieves the latest narrative entry from DynamoDB.
    - Appends the user's action to the narrative and generates the next segment.
    - Stores the updated narrative in DynamoDB with the session ID and a new timestamp.
    
    Args:
    user_id (str): Unique identifier for the user (user email).
    session_id (str): Unique identifier for the session.
    user_action (str): The user's input or action to continue the narrative.

    Returns:
    dict: The updated narrative item.
    """
    # Query the table with both user_id and session_id to ensure the user owns the narrative
    response = narrative_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id) & Key('session_id').eq(session_id)
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
        'user_id': user_id,
        'session_id': session_id,
        'timestamp': timestamp,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'prompt': new_prompt,
        'description': response_text,
        'actions': latest_item.get('actions', []) + [user_action],
        'is_deleted': False
    }
    narrative_table.put_item(Item=new_item)  # Update the item in DynamoDB
    return new_item


def delete_narrative(user_id, session_id):
    """
    Deletes a narrative session from DynamoDB.
    
    Args:
    user_id (str): Unique identifier for the user (user email).
    session_id (str): Unique identifier for the session.
    """
    # Query the table to get all items for the user and session
    response = narrative_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id) & Key('session_id').eq(session_id)
    )

    # Check if any items were found
    if 'Items' not in response or not response['Items']:
        return {"error": "No items found for the given user_id and session_id."}

    # Delete each item
    for item in response['Items']:
        narrative_table.delete_item(
            Key={
                'user_id': user_id,
                'session_id': session_id,
            }
        )

    # TODO: Implement logic to move deleted items to a new table
    #* This will be done in a future update. For now, we'll just log this step
    
    #TODO: Include new table for deleted narratives before permanent deletion
    #* The deleted narratives will be stored here for a short period of time before being permanently deleted
    #* This is to prevent the loss of data and to allow for the retrieval of deleted narratives
    #* The deleted narratives will be moved to this table from the main narrative table
    #* The 'is_deleted' flag will be set to True for the narrative in the main table
    #* The narrative will be moved to the deleted narratives table and given a new timestamp
    
    print(f"TODO: Move deleted items for user {user_id}, session {session_id} to archive table")

    return {"message": f"Successfully deleted narrative session {session_id} for user {user_id}"}


def get_user_narratives(user_id):
    """
    Retrieves all active narratives for a given user from DynamoDB.

    Args:
    user_id (str): The unique identifier for the user (user email).

    Returns:
    list: A list of active narrative items for the user.
    """
    response = narrative_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id),
        FilterExpression=Attr('is_deleted').eq(False)
    )
    items = response.get('Items', [])
    
    # Convert items to JSON-serializable format
    return json.loads(json.dumps(items, default=decimal_default))


def lambda_handler(event, context):
    """
    Handles incoming Lambda events and routes commands to appropriate functions.

    - Supports 'start dreaming', 'continue narrative', 'wake up', 'get narratives',
      and 'save narrative' commands.
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
    session_id = body.get('session_id', 'default_session')
    user_id = body.get('user_id')

    print(f"SESSION_ID: {session_id}")  # Debug log to trace session ID

    # Route the command to the appropriate function
    result = {}
    if command == "start dreaming":
        result = start_narrative(user_id, session_id, dream_description)
    elif command == "continue narrative":
        result = continue_narrative(user_id, session_id, user_action)
    elif command == "wake up":
        result = {"message": "You woke up."}
    elif command == "get narratives":
        result = get_user_narratives(user_id)
    elif command == "delete narrative":
        result = delete_narrative(user_id, session_id)
    else:
        result = {"error": "Unknown command or missing arguments."}

    # Return the result as a JSON response
    return {
        'statusCode': 200,
        'body': json.dumps(result, default=decimal_default)
    }