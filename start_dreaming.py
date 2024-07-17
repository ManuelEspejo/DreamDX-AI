import argparse

from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

CHROMA_PATH = "chroma"

INITIAL_PROMPT_TEMPLATE = """
Based on the following context, generate a descriptive environment for the beginning of a narrative:
{context}

Remember:
- The user reading this is the protagonist, so address them directly, as if they are witnessing it.
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

def start_dreaming():
    dream_description = input("What do you want to dream today? ").strip()
    if not dream_description:
        print("No dream content provided. Cannot start dreaming.")
        return
    start_narrative(dream_description)


def start_narrative(context):
    model = ChatOpenAI()
    prompt_template = ChatPromptTemplate.from_template(INITIAL_PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context)
    description = model.invoke(prompt).content.strip()
    print(f"Human:\nYou open your eyes, this is the first thing that you see...\n\n{description}\n")
    continue_narrative(prompt, context)


def fetch_related_data(context):
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = db.similarity_search_with_relevance_scores(context, k=1)
    return results


def continue_narrative(prompt, context):
    model = ChatOpenAI()
    related_data = fetch_related_data(context)
    related_context = "\n\n".join([doc.page_content for doc, _score in related_data])

    while True:
        user_action = input("Your action: ").strip().lower()
        if user_action == "wake up":
            print("You woke up...")
            break
        new_prompt = f"{prompt}\nUser action: {user_action}\n\n{CONTINUATION_PROMPT_TEMPLATE}\nRelated context: {related_context}\nNarrative continuation: "
        response_text = model.invoke(new_prompt).content.strip()
        print(f"\n\n{response_text}")
        prompt = f"{prompt}\nUser action: {user_action}\n\nNarrative continuation: {response_text}"

def main():
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
