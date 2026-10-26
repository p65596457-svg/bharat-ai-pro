import streamlit as st
from groq import Groq
from PIL import Image
import os
from datetime import datetime

st.set_page_config(page_title="BHARAT AI - PRO MAX", page_icon="🇮🇳", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
now = datetime.now()

st.markdown("<style>.stApp{background:#0e0e0f;} header{visibility:hidden;}</style>", unsafe_allow_html=True)

# Logo
logo = None
for f in ["BHARAT AI (2).png", "BHARAT AI.png", "logo.png"]:
    if os.path.exists(f):
        logo = Image.open(f)
        break
if logo:
    _, c2, _ = st.columns([1,1,1])
    with c2:
        st.image(logo, use_container_width=True)

st.markdown(f"<h1 style='text-align:center;color:white;'>BHARAT AI - PRO MAX</h1><p style='text-align:center;color:gray;'>FS University | By PRINCE | {now.strftime('%d %B %Y')}</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📰 News", "📝 Notes", "🎤 Voice"])

with tab1:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages=[]
        st.rerun()
    if "messages" not in st.session_state:
        st.session_state.messages=[]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if prompt := st.chat_input("Kuch bhi puchho..."):
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            resp = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role":"system","content":"You are BHARAT AI PRO MAX by PRINCE. Answer in Hinglish, helpful and friendly."},
                    {"role":"user","content":prompt}
                ],
            )
            ans = resp.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role
