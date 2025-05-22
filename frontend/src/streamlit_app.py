import streamlit as st
import requests
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure backend URL
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

# Configure requests session with connection pooling
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=10,
    pool_maxsize=10,
    max_retries=3
)
session.mount('http://', adapter)
session.mount('https://', adapter)
session.headers.update({
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Origin': 'https://huggingface.co',
    'Referer': 'https://huggingface.co/'
})

def main():
    st.title("Chat with PDF")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Chat interface
    user_input = st.text_input("Ask a question about your PDF:")
    
    if user_input:
        try:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("Getting response..."):
                # Send message to backend
                response = session.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": user_input},
                    timeout=30
                )
                
                if response.status_code == 200:
                    # Add assistant response to chat
                    st.session_state.messages.append({"role": "assistant", "content": response.json()['response']})
                else:
                    st.error(f"Error: {response.text}")
                    logger.error(f"Chat request failed with status {response.status_code}: {response.text}")
                    
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            logger.error("Chat request timed out")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please check if the server is running.")
            logger.error("Connection error during chat")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"Unexpected error during chat: {str(e)}")
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"👤 You: {message['content']}")
        else:
            st.write(f"🤖 Assistant: {message['content']}")

if __name__ == "__main__":
    main()