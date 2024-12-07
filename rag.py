import os
import re
import json
import numpy as np
import requests
import time
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors

# Set the Hugging Face API token (make sure it's stored securely)
os.environ["HUGGINGFACE_TOKEN"] = "Add your token"
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_TOKEN']}"}  ## Add your "Authorization": ...


# Load and clean the scraped data
def load_scraped_data(scraped_data_file):
    with open(scraped_data_file, 'r', encoding='utf-8') as file:
        scraped_data = json.load(file)

    def clean_markdown(text):
        if not isinstance(text, str):
            return ""
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove images
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # Remove links
        text = ' '.join(text.split())  # Normalize whitespace
        return text

    for entry in scraped_data:
        markdown_content = entry.get("markdown", "")
        entry["cleaned_markdown"] = clean_markdown(markdown_content)
    return scraped_data



# Function to extract contact information from query
def extract_contact_form_info(query):
    form_data = {
        "first_name": re.search(r'First Name:\s*([^\s]+)', query),
        "last_name": re.search(r'Last Name:\s*([^\s]+)', query),
        "email": re.search(r'E-Mail:\s*([^\s]+)', query),
        "message": re.search(r'Message:\s*(.*)', query, re.DOTALL)
    }
    extracted_info = {key: match.group(1).strip() if match else None for key, match in form_data.items()}
    return extracted_info


# Functions to handle memory
def load_memory(memory_file):
    try:
        with open(memory_file, 'r', encoding='utf-8') as f:
            memory = json.load(f)
    except FileNotFoundError:
        memory = []
    return memory


def save_memory(memory, memory_file):
    with open(memory_file, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)


# Function to handle API request with retry logic
def send_to_huggingface_api(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def send_with_retry(payload, max_retries=10, wait_time=30):
    retries = 0
    while retries < max_retries:
        response = send_to_huggingface_api(payload)
        if 'error' in response and 'loading' in response['error']:
            estimated_time = response['error'].get('estimated_time', wait_time)
            print(f"Model is loading, retrying in {wait_time} seconds... ({estimated_time} seconds estimated)")
            time.sleep(wait_time)
            retries += 1
        else:
            return response
    return {"error": "Model failed to load after multiple retries."}


# The main RAG pipeline function
def rag_pipeline(query, sentence_model, index, scraped_data, memory):
    # Parse the query and extract contact form information
    contact_info = extract_contact_form_info(query)

    # Encode the cleaned query and retrieve relevant documents
    cleaned_query = query
    query_embedding = sentence_model.encode(cleaned_query)

    # Retrieve top-k relevant documents using NearestNeighbors
    k = 3
    distances, indices = index.kneighbors([query_embedding], n_neighbors=k)
    retrieved_docs = [scraped_data[i] for i in indices[0]]

    # Combine retrieved documents into a single context
    context = " ".join([doc['cleaned_markdown'][:1500] for doc in retrieved_docs])
    context += " 27.10.2024"  # Adjust as per your requirement

    # Build conversation history from memory
    conversation_history = ''
    for turn in memory[-3:]:  # Limit to last 3 interactions
        conversation_history += f"User: {turn['query']}\nAssistant: {turn['response']}\n"


    #
    # Create a prompt for the email response, including conversation history
    prompt = f"""
    The following is a conversation between a user and an assistant.

    {conversation_history}
    User: "{cleaned_query}"
    Only if user asks something related to hiking equipment shopping (e.g. Warranty problems,Refund,Order Modification,Payment problem, Subscription, Discounts, Delivery times) otherwise answer like I am afraid I cannot assist you regarding your question our customer support team will reach you to given e-mail if necessary. For further questions user can reach customer support team from support@peakcommerce.ch.
    Use the context provided below to craft a professional response as an email.
    Context:
    {context}
    Email format:
    - The answer must start with a greeting (e.g., "Dear [name],")
    - Include a clear response addressing the user's query.
    - The answer must end with a greeting (e.g., "Best regards, \nYour PeakCommerce Team" or "Sincerely, \n Your PeakCommerce Team")
    - No more text after this.
    Answer:
    """
    # Send the prompt to Hugging Face API
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,  #
            "stop": ["Best regards, \nYour PeakCommerce Team"],
            "temperature": 0.9,
            "length_penalty":1.0
        }
    }
    api_response = send_with_retry(payload)

    # Extract and return the generated response
    if 'error' in api_response:
        return f"Error: {api_response['error']}"
    generated_response = api_response[0]['generated_text'][len(prompt):]
    return generated_response.strip()


# Load sentence transformer model and scraped data
def setup_pipeline(scraped_data_file):
    sentence_model = SentenceTransformer('all-mpnet-base-v2')
    scraped_data = load_scraped_data(scraped_data_file)
    # Generate embeddings
    embeddings = np.array([sentence_model.encode(entry['cleaned_markdown']) for entry in scraped_data])
    dimension = embeddings.shape[1]
    # Initialize NearestNeighbors index
    index = NearestNeighbors(n_neighbors=3, metric='euclidean')
    index.fit(embeddings)
    return sentence_model, index, scraped_data


# Main execution function to take user query and return generated answer
def get_email(query):
    # Setup models and data
    sentence_model, index, scraped_data = setup_pipeline('emails_generated.json')

    # Load memory
    memory = load_memory('memory.json')

    # Get the generated answer
    generated_answer = rag_pipeline(query, sentence_model, index, scraped_data, memory)

    # Update memory
    memory.append({'query': query, 'response': generated_answer})
    save_memory(memory, 'memory.json')

    return generated_answer


if __name__ == "__main__":
    # Example query
    user_query = "The hiking gear I ordered was delivered damaged. What steps should I take to file a complaint and get a replacement?"
    # Get the email response
    response = get_email(user_query)
    # Print the generated response
    print(response)
