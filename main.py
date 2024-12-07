import streamlit as st
from rag import get_email
import base64

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# dictionary with roles
def new_chat():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


message_style = """
    <style>
    .chat-box {
        display: flex;
        align-items: flex-start;
        margin-bottom: 15px;
    }
    .chat-icon {
        background-color: #f5f5f5;
        color: #ffffff;
        border-radius: 50%;
        padding: 10px;
        margin-right: 15px;
        font-size: 20px;
        height: 50px;
        width: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .chat-message {

        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        width: 100%;
        box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.2);
    }
    body {
        background-color: #D84B50;
        padding-top: 0px;   /* Remove padding from the top of the page */
        margin-top: 0px;    /* Remove margin from the top of the page */
    }
    .main-container {
        background-color: white;
        width: 60%;  /* Adjust this to control the width of the white box */
        margin: 0 auto;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.2);
    }
    .image-container img {
        margin: 0;  /* Remove margin */
        padding: 0; /* Remove padding */
        display: block;  /* Ensure the image takes the full width */
    }
    </style>
"""

st.markdown(message_style, unsafe_allow_html=True)

# Title
# Center the image and title using HTML and markdown
col1, col2 = st.columns([4, 1])
with col1:
    st.title("PeakCommerce Chatbot")
    st.caption("PeakCommerce Customer Support")
# st.write("Feel free to send us your message using the form below.")
with col2:
    st.image("PeakCommerce_Logo.jpg", width=150)

# Info
st.markdown(
    """
    <div>
    <strong>Do you need help or have any questions?</strong><br>
    Please use the form below to share your request.<br><br>
    For simpler inquiries, our Chatbot will provide a quick response, while more detailed or personal questions will be forwarded to our team for personalized support.
    This ensures that our responses are as quick as possible!<br><br>
    </div>
    """,
    unsafe_allow_html=True
)

# Text area

# First Name and Last Name share the same line
col3, col4 = st.columns(2)
with col3:
    first_name = st.text_input("First Name")
with col4:
    last_name = st.text_input("Last Name")

email = st.text_input("E-Mail")

# Message field takes the full width as a large box (keeping it as a text area)
message = st.text_area("Message", height=200)

# Concatenate the inputs into a single string
concatenated_text = f"""
First Name: {first_name}
Last Name: {last_name}
E-Mail: {email}
Message: {message}
"""


# Function to trim the response
def trim_response(response):
    # Find the index of "Your PeakCommerce Team" to remove anything after it
    split_marker = "Your PeakCommerce Team"

    if split_marker in response:
        response = response.split(split_marker)[0] + split_marker

    # Find the index of "Dear" and remove anything before it
    dear_marker = "Dear"

    if dear_marker in response:
        response = response.split(dear_marker, 1)[1]  # Keep everything starting from "Dear"
        response = dear_marker + response  # Re-add "Dear" at the beginning

    return response


# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Convert the PeakCommerce logo to base64
image_path = "PeakCommerce_Logo.jpg"  # Adjust the path as needed
logo_base64 = image_to_base64(image_path)

# Handle button click for form submission
if st.button("Submit"):
    # Generate the response only after the button is clicked
    with st.spinner("Thinking..."):
        response = get_email(concatenated_text)  # Assuming this function processes the input

    # Display only the assistant's response
    trimmed_response = trim_response(response)
    # Create a custom chat message display with icon
    formatted_response = f"""
    <div class="chat-box">
        <div class="chat-icon">
            <img src="data:image/jpeg;base64,{logo_base64}" alt="Assistant Icon">
        </div>
        <div class="chat-message">
            {trimmed_response.replace('\n', '<br>')}
        </div>
    </div>
    """

    # Display the styled response
    st.markdown(formatted_response, unsafe_allow_html=True)
