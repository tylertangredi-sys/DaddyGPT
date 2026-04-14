import streamlit as st
from openai import OpenAI

# Setup the Page
st.set_page_config(page_title="Dual-Mode AI", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Dual-Mode AI")

# Sidebar for Config
with st.sidebar:
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    mode = st.radio("Choose Mode:", ["Normal", "Unhinged"])
    uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Image ready.")

# Define AI Personalities
system_prompts = {
    "Normal": "You are a helpful, polite, and concise assistant.",
    "Unhinged": "You are a chaotic, brutally honest, and wild AI. Use slang, be sarcastic, and don't hold back your 'opinions' (within safety guidelines)."
}

client = OpenAI(api_key=api_key) if api_key else None

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    if not api_key:
        st.error("Please add your API Key in the sidebar!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build the message for the API
        content = [{"type": "text", "text": prompt}]
        
        # If an image is uploaded, it gets attached here (simplified)
        # Note: In a real app, you'd convert the image to Base64 first.

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompts[mode]},
                    {"role": "user", "content": prompt}
                ],
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

