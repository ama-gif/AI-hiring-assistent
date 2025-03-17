import streamlit as st
import os
from chat_manager import ChatManager
from data_validator import validate_email, validate_phone
import time

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_step" not in st.session_state:
    st.session_state.current_step = "greeting"
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()

# App title and description
st.title("TalentScout Hiring Assistant")
st.markdown("""
Welcome to TalentScout's AI Hiring Assistant! I'm here to help with your initial screening process.
Let's get to know you better and discuss your technical expertise.
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show thinking indicator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Process the message based on current step
            response = st.session_state.chat_manager.process_message(
                prompt, 
                st.session_state.current_step,
                st.session_state.candidate_info
            )
            
            # Update session state based on response
            if response.get("new_step"):
                st.session_state.current_step = response["new_step"]
            if response.get("candidate_info"):
                st.session_state.candidate_info.update(response["candidate_info"])
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response["message"]})
            st.markdown(response["message"])

            # If the conversation is complete, show summary
            if st.session_state.current_step == "complete":
                st.success("Interview completed! Thank you for your time.")
                st.json(st.session_state.candidate_info)

# Add reset button
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.current_step = "greeting"
    st.session_state.candidate_info = {}