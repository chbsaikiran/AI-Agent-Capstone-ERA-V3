import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Backend API URL - replace with your EC2 instance URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://your-ec2-instance:5000")

st.title("PDF Chat Application")

# File upload section
uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

if uploaded_file is not None:
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Prepare the file for upload
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
        
        # Send file to backend with timeout
        status_text.text("Uploading file...")
        response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files,
            timeout=30  # 30 seconds timeout
        )
        
        # Update progress
        progress_bar.progress(100)
        
        if response.status_code == 200:
            st.success("File uploaded successfully!")
        else:
            st.error(f"Error uploading file: {response.text}")
    except requests.exceptions.Timeout:
        st.error("Upload timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server. Please check if the server is running.")
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
    finally:
        # Clear progress bar and status
        progress_bar.empty()
        status_text.empty()

# Chat interface
st.subheader("Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Send message to backend
    try:
        with st.spinner("Waiting for response..."):
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"message": prompt},
                timeout=30  # 30 seconds timeout
            )
        
        if response.status_code == 200:
            bot_response = response.json()["response"]
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(bot_response)
        else:
            st.error(f"Error getting response: {response.text}")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server. Please check if the server is running.")
    except Exception as e:
        st.error(f"Error: {str(e)}") 