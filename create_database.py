import os
import shutil
from dotenv import load_dotenv

import openai
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

