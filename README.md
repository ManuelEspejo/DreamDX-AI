# DreamDX AI

## Overview

**DreamDX AI** is an innovative application designed to allow you to revisit and take control of your dreams. Powered by advanced AI, this app generates interactive scenarios based on your past dreams, creating personalized simulations where the narrative continues seamlessly from where it left off.

Imagine stepping back into a dream, but this time with full awareness and control. Explore different scenarios, unlock new possibilities, and navigate through the depths of your inner world with the knowledge that you're in a dream.

### Technologies Used

- **Streamlit** - for the user interface.
- **AWS** - Lambda and API Gateway for backend logic and API handling.
- **OpenAI** - GPT-4o-mini API (via LangChain) for narrative generation.
- **DynamoDB** - to store and manage dream sessions and narratives.
- **Boto3** - for interaction with AWS DynamoDB from Python.

## Installation and Setup Instructions

### Prerequisites

- Local Virtual Enviroment
- Python 3.x installed on your system.
- An AWS account with permissions to create and manage resources like Lambda, API Gateway, and DynamoDB.
- OpenAI credentials (account and API Key) or other model API key of your choice.

### Configurations

*Documentation in process...*

## Project Structure

```bash
/DreamDX-AI
│
├── /config/
│   ├── .env.example              # Example environment variable configuration
│   └── aws-llm-requirements.txt  # Dependencies for the Lambda function llm layer
│
├── /data/                        # Directory for test data (ignored in git)
│
├── /src/
│   ├── /backend/
│   │   └── lambda_functions/
│   │       ├── start_dreaming.py  # Main script for the AWS Lambda function
│   │       └── api.py             # Script for handling API calls
│   │
│   └── /frontend/
│       └── app.py                 # Main script for the Streamlit application
│
├── /tests/                        # (Optional) Unit and integration tests
│
├── LICENSE                        # MIT License for the project
├── README.md                      # This file
├── requirements.txt               # Dependencies for development and interface
└── .gitignore                     
```

## Roadmap

*Documentation in process...*
