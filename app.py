import streamlit as st
from groq import Groq
from PIL import Image
import os
from datetime import datetime
import requests

st.set_page_config(page_title="BHARAT AI - PRO MAX", page_icon="🇮🇳", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
now = datetime.now()

st.markdown("<style>.stApp{background:#0e0e0f;} header{visibility:hidden;}</style>", unsafe_allow_html=True)

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

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Chat", "News", "Notes", "Voice", "Image Gen"])

with tab1:
    if st.button("Clear Chat"):
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
                    {"role":"system","content":"You are BHARAT AI PRO MAX by PRINCE. Answer in Hinglish."},
                    {"role":"user","content":prompt}
                ],
            )
            ans = resp.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role":"assistant","content":ans})

with tab2:
    st.subheader("Taaza News")
    q = st.text_input("Konsi news?", "India latest news", key="n1")
    if st.button("News Lao"):
        r = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content":f"Latest news about {q} today. Give 7 points in Hinglish"}])
        st.markdown(r.choices[0].message.content)

with tab3:
    st.subheader("Notes Maker")
    topic = st.text_input("Topic?", key="n2")
    if st.button("Notes Banao"):
        r = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content":f"Make detailed notes on {topic} in Hinglish"}])
        st.markdown(r.choices[0].message.content)

with tab4:
    st.subheader("Voice se Puchho")
    st.info("Mic dabao, bolo!")
    audio = st.audio_input("Bolo kuch...")
    if audio:
        with st.spinner("Sun raha hu..."):
            try:
                transcription = client.audio.transcriptions.create(
                    file=("audio.wav", audio.getvalue()),
                    model="whisper-large-v3",
                    response_format="text"
                )
                st.success(f"Tune bola: {transcription}")
                resp = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role":"user","content":transcription}]
                )
                st.markdown(resp.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

with tab5:
    st.subheader("AI Image Generator")
    img_prompt = st.text_input("Kaisi image chahiye?", "Indian robot with flag, 4k", key="img")
    if st.button("Image Banao"):
        if img_prompt:
            with st.spinner("Bana raha hu..."):
                url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(img_prompt)}?width=1024&height=1024&nologo=true"
                st.image(url, caption=img_prompt, use_container_width=True)
                st.markdown(f"[Download]({url})")
