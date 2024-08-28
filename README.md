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
├── /components/
│   ├── __init__.py
│   ├── api.py
│   ├── auth.py
│   └── dream_handler.py
│
├── /config/
│   ├── .env
│   ├── .env.example
│   └── aws-llm-requirements.txt
│
├── /data/
│
├── /pages/
│   └──_🤖​💬_Dream_Simulator.py
│
├── /tests/
│
├── .gitignore
├── Home.py
├── LICENSE
├── README.md
└── requirements.txt
                
```

## Roadmap

*Documentation in process...*

### MVP

**Simplicity and Accessibility**: Focus on ensuring that the initial version of the app is easy to use, with minimal technical knowledge required. This includes a simple and intuitive UI that guides the user through the simulation process.

- [x] ~~**API Integration**: Integrate the backend API to handle dream narrative generation.~~

- [x] ~~**Streamlit UI Implementation**: Set up the basic user interface using Streamlit.~~
  - [x]  ~~**Chat Interface**: Implement a chat interface for the user to interact with the simulation.~~
  - [x] ~~**Wake-Up Simulation**: Implement a basic wake-up mechanism to end the simulation and reset the session.~~
  - [X] ~**API Connection**: Implement API integrations with streamlit.~
- [ ] **Demonstrative Templates:** Include templates with demonstration data so that users can try the application without needing to upload their own data.

#### Data Management

- [x] ~~**Basic DynamoDB Integration**: Implement initial DynamoDB setup to store and manage dream sessions.~~
- [x] **Implementation of the authentication system**: Develop the authentication system using AWS Cognito to manage unique user session records.
- [ ] **Enhanced session management**: Implement improvements in the handling of generated narratives and user sessions.
- [ ] **Past Dream Database**: Implement a database for users to store past dreams data.
- [ ] **Data Upload Feature**: Implement the ability for users to upload dreams directly from text files (e.g., .txt or .md), making it easier for them to integrate past dreams into the simulation.

### Upcoming Features

<details>
<summary>Expand for more info</summary>

#### Enhanced Data Handling

- [ ] **Structured Outputs**: Add a feature for structured outputs from OpenAI to process data like dream signals and other relevant elements in various ways.
- [ ] **Expanded Dream Memory**: Implement a feature allowing users to upload past dreams so that the model can explore them when generating a narrative, based on a similarity metric to enhance personalization.

#### Personalization and User Interaction

- [ ] **User Profile and Dreamer Sheet**: Develop a basic user profile system where users can input key characteristics that will influence the dream simulation, such as their name, recurring dream symbols, or specific goals for their dream exploration.
  - [ ] Experiment and define the most important data for a personalized experience.
- [ ] **Initial Dream Signal Analysis**: Start implementing a system to analyze and highlight key dream signals during the simulation. These signals could be personal symbols or recurring themes that the AI will mark as relevant during the narrative.

#### Privacy and Security

- [ ] **Privacy Controls**: Ensure that basic privacy features are in place, such as allowing users to manage who has access to their dream data and whether the data is processed locally or via an API.
- [ ] **Censorship Toggle**: Implement an option for users to toggle censorship on or off during dream simulations, ensuring that the content is as realistic or as safe as the user prefers.

#### User Experience and Feedback

- [ ] **Post-Simulation Analysis**: Begin working on a basic feedback mechanism that provides users with a summary or analysis of their dream simulation once it ends. This could include key themes, actions taken, and potential insights.
- [ ] **Simulation Feedback Loop**: Create a simple feedback loop where users can rate the accuracy or relevance of the simulation, which will help refine future iterations of the AI’s behavior.
- [ ] **Enhanced Wake-Up Feature**: Add visual and interactive elements to the wake-up process, such as a fading screen or a prompt that asks "What did you dream about today?" to enhance user immersion.

</details>

### Short-Term Objectives

<details>
<summary>Expand for more info</summary>

- **Dream Signal Analysis**: Implement a system to analyze dream signals during the narrative. All your personal dream signals will be marked as relevant items during generation, and can be selected to gather statistics and insights on their influence in your past dreams, along with other relevant characteristics for the user.
- **Dreamer Profile**: Develop a profile system to include the user's unique characteristics, allowing the model to understand the most relevant details that could influence the dream. This will focus on creating a dream profile and defining personal goals for dream exploration.
- **Expand Model Selection**: While currently working with the OpenAI API, the goal is to extend support to other types of models, particularly local open-source models that offer the desired privacy for users who prioritize it.

</details>

### Long-Term Objectives

<details>
<summary>Expand for more info</summary>

The ultimate goal of DreamDX AI is to transform it into a fundamental tool for dream exploration—the tool I wish I had during my own journey of inner exploration. DreamDX AI aims to provide a personalized, private, and immersive experience that adapts to each user's unique dreamscape and goals.

#### Potential Uses

- Therapeutic applications
- Self-analysis and self-discovery
- Dream research
- Lucid dreaming exploration
- Creative inspiration

To achieve this, DreamDX AI must excel in three key areas:

##### 1. **Personalization**

DreamDX AI should be highly customizable, getting to know each user intimately and understanding their goals in dream exploration. This will allow it to create unique scenarios tailored to achieve those goals. Some key points:

- **Advanced Dreamer Profile**: Continue to develop the Dreamer Profile system, allowing it to evolve with more data inputs, such as emotional states, personal milestones, and long-term dream patterns. This profile will not only influence the dream simulations but also adapt to the user's growth and changes over time.
- **Adaptive Simulation**: Implement a system where the AI learns from each user's interactions, continually refining the dream generation process. This could include personalized prompts based on past dream experiences or adjustments to the narrative flow to better match the user's preferences.
- **Wearables and Integration**: Explore the possibility of integrating with other personal data sources (e.g., fitness trackers, mood journals) to create a more holistic understanding of the user's mental and physical state, further enhancing dream personalization.

##### 2. **Privacy**

Ensuring user privacy is paramount, particularly given the intimate nature of dream content. DreamDX AI must be designed with robust privacy features from the ground up:

- **Local Data Processing (Optional depending on user needs)**: Prioritize the use of local, open-source AI models that allow users to process their data entirely on their devices, without reliance on external servers. This ensures that the dream data remains private and secure. 
- **Encrypted Dream Storage**: Develop and implement advanced encryption methods for storing dream data, ensuring that only the user can access and manage their dream archives.
- **User-Controlled Sharing**: Introduce granular controls that allow users to decide what data, if any, they wish to share. This could include sharing specific dream insights with therapists or researchers in a secure and anonymized format.

##### 3. **Immersion**

The ultimate aim is to create an experience that is as close to a lucid dream as possible, blending AI-powered universe generation with cutting-edge immersive technologies:

- **AI-Driven Universe Generation**: Integrate advanced AI models capable of generating highly detailed and interactive dream environments. These environments should respond dynamically to the user's actions, making each simulation unique and deeply engaging.
- **Virtual Reality Integration**: Explore the integration of DreamDX AI with virtual reality platforms to enhance the sensory experience. This could involve full VR simulations where users can "walk through" their dreams, interacting with elements in a fully immersive 3D space.
- **Sensory Feedback Systems**: Investigate the potential for haptic feedback and other sensory technologies that can simulate physical sensations within the dream environment, further blurring the line between the dream and reality.
</details>