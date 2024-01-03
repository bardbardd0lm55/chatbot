from openai import OpenAI
import streamlit as st



logo_url= "https://lawyerchat.tech/wp-content/uploads/2023/12/cropped-lawyerchat-tech-logo.png"

# Display the logo
st.image(logo_url, width=500)  # You can adjust the width as needed

# Initialize the OpenAI client
openai = OpenAI(
    api_key="API_KEY_",
    base_url="https://api.deepinfra.com/v1/openai"
)

# Function to get response from OpenAI
def get_openai_response(message_history):
    chat_completion = openai.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=message_history
    )
    return chat_completion.choices[0].message.content

# Function to send the message and get response
def send_message():
    user_message = {"role": "user", "content": st.session_state.user_input}
    st.session_state.history.append(user_message)

    # Get response from OpenAI
    openai_response = get_openai_response(st.session_state.history)
    st.session_state.history.append({"role": "assistant", "content": openai_response})
    st.session_state.user_input = ""
    
# Store conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

# Display conversation history in main area
for message in st.session_state.history:
    # Using Markdown for message content
    st.markdown(f"**{message['role'].title()}**: {message['content']}")

# Input box and Send button at the bottom in main area
st.text_input("Your Input Below: ", key="user_input", on_change=send_message, value="")
