from openai import OpenAI
import streamlit as st
from streamlit_javascript import st_javascript

API_KEY_ = 'ABCD'

#Custom css for components styling
with open('css/styles.css') as f:
  st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")

#Dark & Light logos
black_logo_url = "https://lawyerchat.tech/wp-content/uploads/2023/12/cropped-lawyerchat-tech-logo.png"
white_logo_url = "https://lawyerchat.tech/wp-content/uploads/2024/01/lawyerchat-tech-logo-white.png"

# Display the logo
if st_theme == "dark":
  st.markdown('<h1 class="text-center"><img src="'+white_logo_url+'" height="60px"></h1>', unsafe_allow_html= True)
else:
  st.markdown('<h1 class="text-center"><img src="'+black_logo_url+'" height="60px"></h1>', unsafe_allow_html= True)

# Initialize the OpenAI client
openai = OpenAI(
    api_key=API_KEY_,
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
st.text_input("What are you looking for? ", key="user_input", on_change=send_message, value="")

#Display the footer/credit
st.markdown('<p style="font-size: 12px; color: #666;" class="text-center mt-5 mb-4" id="credit-area">LawyerChat v0.1.2<br>All Rights Reserved © LawyerChat 2024</p>', unsafe_allow_html= True)

st.markdown('<script>setInterval(function(){ console.log(window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")); }, 3000)</script>', unsafe_allow_html= True)
