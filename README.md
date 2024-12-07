# email_automation

Here’s a README file tailored for your email automation system with a Streamlit UI:

Email Automation with Streamlit UI
This project implements a Response-Augmented Generation (RAG) pipeline for handling customer email queries. It leverages Hugging Face LLMs and sentence transformers to process user inputs, retrieve relevant information, and generate email responses. The system is designed to interact seamlessly through a Streamlit UI for user-friendly access.

Features
AI-Powered Email Automation: Uses Hugging Face's LLMs to generate professional email responses.
RAG Pipeline: Combines semantic search with transformer models for accurate context-based responses.
Dynamic Context Retrieval: Retrieves relevant knowledge from scraped data for custom responses.
Contact Information Parsing: Extracts essential information like name, email, and message from user input.
Memory Integration: Maintains conversation history for contextual continuity.
Streamlit UI: Easy-to-use graphical interface for input and response visualization.



Here’s a README file tailored for your email automation system with a Streamlit UI:

Email Automation with Streamlit UI
This project implements a Response-Augmented Generation (RAG) pipeline for handling customer email queries. It leverages Hugging Face LLMs and sentence transformers to process user inputs, retrieve relevant information, and generate email responses. The system is designed to interact seamlessly through a Streamlit UI for user-friendly access.

Features
AI-Powered Email Automation: Uses Hugging Face's LLMs to generate professional email responses.
RAG Pipeline: Combines semantic search with transformer models for accurate context-based responses.
Dynamic Context Retrieval: Retrieves relevant knowledge from scraped data for custom responses.
Contact Information Parsing: Extracts essential information like name, email, and message from user input.
Memory Integration: Maintains conversation history for contextual continuity.
Streamlit UI: Easy-to-use graphical interface for input and response visualization.



File Structure
main.py: The main entry point for running the RAG pipeline and Streamlit UI.
rag.py: Contains the RAG pipeline logic for query processing and response generation.
emails_generated.json: The dataset of pre-scraped and cleaned email information.
memory.json: Persistent memory storage for maintaining conversation history.
app.log: Logs system activities for debugging purposes.
PeakCommerce_Logo.jpg: Brand logo for the Streamlit UI.
README.md: Documentation file for the project.
How It Works
User Query Input: Users provide their queries via the Streamlit UI.
Information Extraction: Key contact information is parsed from the query.
Contextual Search: The system retrieves relevant data from emails_generated.json using semantic similarity.
LLM Processing: The query and context are sent to Hugging Face's API for generating the email response.
Memory Updates: The interaction is saved to memory.json for future reference.
