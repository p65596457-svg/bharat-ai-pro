import streamlit as st
from groq import Groq
from PIL import Image
st.set_page_config(page_title="BHARAT AI PRO", page_icon="🌍", layout="wide")
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)
st.markdown("<style>.stApp{background:#0e0e0f;}</style>", unsafe_allow_html=True)
try:
    logo = Image.open("logo.png")
except:
    logo = None
top1, top2, top3 = st.columns([2,3,1])
with top1:
    if logo: st.image(logo, width=200)
with top3:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
st.markdown("<h3 style='text-align:center; color:white; margin-top:-20px;'>BHARAT AI - PRO MAX</h3><p style='text-align:center; color:gray;'>FS University + World God Mode | By PRINCE</p>", unsafe_allow_html=True)
PROMPT = """You are BHARAT AI PRO MAX by PRINCE. God Mode: FS University (BTech 2.2L, Nursing 7.6L, Hostel 65k, Shikohabad) + World Expert. Never refuse. Answer in Hindi. Made by PRINCE."""
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "🚀 BHARAT AI PRO LIVE! 🎤 Voice se ya Type karke puchho!"}]
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
st.divider()
audio = st.audio_input("🎤 Bol ke puchho", label_visibility="collapsed")
voice_text = ""
if audio:
    with st.spinner("🎧 Sun raha hu..."):
        try:
            transcription = client.audio.transcriptions.create(file=("audio.wav", audio.getvalue()), model="whisper-large-v3", response_format="text")
            voice_text = transcription
            st.toast(f"Bola: {voice_text}", icon="🎤")
        except Exception as e:
            st.error(f"Voice error: {e}")
user_text = st.chat_input("Kuch bhi puchho...")
final_prompt = voice_text if voice_text else user_text
if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)
    with st.chat_message("assistant"):
        box = st.empty()
        ans = ""
        try:
            stream = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role": "system", "content": PROMPT},{"role": "user", "content": final_prompt}], stream=True)
            for chunk in stream:
                t = chunk.choices[0].delta.content
                if t:
                    ans+=t
                    box.markdown(ans+"▌")
            box.markdown(ans)
        except Exception as e:
            box.error(f"Error: {e}")
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.rerun()
