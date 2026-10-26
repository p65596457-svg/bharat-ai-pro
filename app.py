import streamlit as st
from groq import Groq
from PIL import Image
import os

st.set_page_config(page_title="BHARAT AI - PRO MAX", page_icon="🇮🇳", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.markdown("<style>.stApp{background:#0e0e0f;} header{visibility:hidden;}</style>", unsafe_allow_html=True)

logo = None
for f in ["BHARAT AI (2).png", "BHARAT AI.png", "logo.png"]:
    if os.path.exists(f):
        logo = Image.open(f)
        break

# BILKUL CENTRE LOGO
if logo:
    _, mid, _ = st.columns([1,1,1])
    with mid:
        st.image(logo, use_container_width=True)

st.markdown("<h1 style='text-align:center;color:white;'>BHARAT AI - PRO MAX</h1><p style='text-align:center;color:gray;'>FS University + World God Mode | By PRINCE</p>", unsafe_allow_html=True)

if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages=[]
    st.rerun()
st.divider()

if "messages" not in st.session_state: st.session_state.messages=[]
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Kuch bhi puchho..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    resp = client.chat.completions.create(model="llama3-8b-8192", messages=[{"role":"user","content":prompt}])
    ans = resp.choices[0].message.content
    with st.chat_message("assistant"): st.markdown(ans)
    st.session_state.messages.append({"role":"assistant","content":ans})
