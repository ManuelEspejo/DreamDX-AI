import os
import shutil

import openai
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables. (OpenAI API key from .env file)
load_dotenv()
# Set OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma"
DATA_PATH = "data/dreams"
CHUNK_SIZE = 4000  # Define the threshold for chunking

def main():
    """
    Main function to generate the data store.
    """
    generate_data_store()


def generate_data_store():
    """
    Function to generate the data store by loading documents,
    splitting text into chunks, and saving to Chroma.
    """
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents() -> list[Document]:
    """
    Load the data from the data folder.
    
    Returns:
    List of loaded documents.
    """
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]) -> list[Document]:
    """
    Create small chunks from long documents or keep short documents intact
    for better dream context.
    
    Args:
        documents: List of documents to be split.
    
    Returns:
        List of document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = []

    for doc in documents:
        if len(doc.page_content) > CHUNK_SIZE:
            # Split document into chunks
            doc_chunks = text_splitter.split_documents([doc])
            chunks.extend(doc_chunks)
        else:
            # Add the whole document as a single chunk
            chunks.append(doc)

    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # # For debugging purposes: print a sample chunk
    # if chunks:
    #    document = chunks[10] if len(chunks) > 10 else chunks[0]
    #    print(document.page_content)
    #    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    """
    Save document chunks to Chroma vector store.
    
    Args:
    chunks: List of document chunks to be saved.
    """
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    Chroma.from_documents(chunks,
                          OpenAIEmbeddings(),
                          persist_directory=CHROMA_PATH)
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()