import argparse
import random

from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

CHROMA_PATH = "chroma"

INITIAL_PROMPT_TEMPLATE = """
Based on the following context, generate a descriptive environment for the beginning of a narrative:


{context}

Remember:
The user reading this is the protagonist, so address them directly, as if they are witnessing it.
You should keep the narrative short but informative about the scene, no more than 100 words.
---

Description:
"""

ROLEPLAY_PROMPT_TEMPLATE = """
What do you do next?
"""

def start_dreaming():
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Fetch some data for the simulation using a broad query.
    broad_query = "general context"  # This should be broad enough to retrieve multiple documents.
    results = db.similarity_search_with_relevance_scores(broad_query, k=5)
    if len(results) == 0:
        print("No data available in the database to start dreaming.")
        return

    # Randomly select a few documents to use as initial context.
    initial_docs = random.sample(results, min(len(results), 1))
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in initial_docs])

    # Start the narrative.
    start_narrative(context_text)

def start_narrative(context):
    # Create a descriptive environment setup using the context.
    model = ChatOpenAI()
    prompt_template = ChatPromptTemplate.from_template(INITIAL_PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context)
    description = model.invoke(prompt).content.strip()

    # Print the initial description to the user.
    print(f"Human:\nYou open your eyes, this is the first thing that you see...\n\n{description}\n")

    # Continue with the roleplay.
    continue_narrative(prompt)

def continue_narrative(prompt):
    model = ChatOpenAI()

    while True:
        # Get user input for the next action.
        user_input = input("Your action: ").strip().lower()
        
        if user_input == "wake up":
            print("You woke up...")
            break
        
        # Generate the next part of the narrative.
        new_prompt = f"{prompt}\nUser action: {user_input}\nNarrative continuation: "
        response_text = model.invoke(new_prompt).content
        print(f"\n\n{response_text}")

        # Update the prompt with the new user action and model response.
        prompt = f"{prompt}\nUser action: {user_input}\nNarrative continuation: {response_text}"

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="The command to execute.")
    args = parser.parse_args()
    command = args.command.lower()

    if command == "start dreaming":
        start_dreaming()
    elif command == "wake up":
        print("You woke up...")
    else:
        print("Unknown command. Please use 'start dreaming' or 'wake up'.")

if __name__ == "__main__":
    main()

