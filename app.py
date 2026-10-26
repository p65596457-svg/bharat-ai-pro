import streamlit as st
from groq import Groq
from PIL import Image
import os
from datetime import datetime
import pytz
import calendar

st.set_page_config(page_title="BHARAT AI - PRO MAX", page_icon="🇮🇳", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.markdown("<style>.stApp{background:#0e0e0f;} header{visibility:hidden;} .stTabs [data-baseweb='tab']{color:white;}</style>", unsafe_allow_html=True)

logo = None
for f in ["BHARAT AI (2).png", "BHARAT AI.png", "logo.png"]:
    if os.path.exists(f):
        logo = Image.open(f)
        break
if logo:
    _, mid, _ = st.columns([1,1,1])
    with mid: st.image(logo, use_container_width=True)

st.markdown(f"<h1 style='text-align:center;color:white;margin-bottom:0;'>BHARAT AI - PRO MAX</h1><p style='text-align:center;color:gray;'>FS University | By PRINCE | 📅 {now.strftime('%d %B %Y')} | ⏰ LIVE IST</p>", unsafe_allow_html=True)

# Live clock
st.components.v1.html(f"""
<div style='text-align:center;color:#FFD700;font-family:monospace;'><div style='font-size:20px;font-weight:bold;' id='t'></div></div>
<script>function u(){{const n=new Date();document.getElementById('t').innerHTML='⏰ '+n.toLocaleTimeString('en-IN',{{timeZone:'Asia/Kolkata',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:true}})+' IST - LIVE'}}setInterval(u,1000);u();</script>
""", height=45)

# TABS - Ye naya feature hai
tab1, tab2, tab3 = st.tabs(["💬 Chat - Kuch bhi Puchho", "📰 Live News", "📝 Notes Maker"])

with tab1:
    if st.button("🗑️ Clear Chat", key="c1"): 
        st.session_state.messages=[]
        st.rerun()
    
    if "messages" not in st.session_state: st.session_state.messages=[]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Kuch bhi puchho... News, Notes, Date, Time..."):
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                resp = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role":"system","content":f"You are BHARAT AI PRO MAX by PRINCE, FS University. Today is {now.strftime('%d %B %Y %A %I:%M %p IST')}. You are God Mode AI. You can answer ANYTHING: News, Notes, Study Material, Current Affairs, Science, History, Coding, Date/Time calculation. If user asks date, calculate accurate day. If asks news, give latest possible info. Answer in Hinglish, friendly, powerful."},
                        {"role":"user","content":prompt}
                    ],
                )
                ans = resp.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role":"assistant","content":ans})
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("📰 Aaj ki Taaza News")
    news_topic = st.text_input("Konsi news chahiye? (e.g. India, Sports, Tech, World)", "India latest news today")
    if st.button("🔍 News Lao", use_container_width=True):
        with st.spinner("News la raha hu..."):
            try:
                r = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role":"system","content":f"Today is {now.strftime('%d %B %Y')}. You are a news expert. Give latest news summary on given topic. Give 5-7 points, crisp, in Hindi/English. Mention you are giving based on latest knowledge."},
                        {"role":"user","content":f"Give me latest news about: {news_topic}"}
                    ]
                )
                st.success("Taaza Khabar:")
                st.markdown(r.choices[0].message.content)
            except Exception as e:
                st.error(str(e))

with tab3:
    st.subheader("📝 Notes Maker - Kisi bhi topic ke notes")
    topic = st.text_input("Topic likho (e.g. Photosynthesis, Indian Constitution, AI)")
    level = st.selectbox("Level", ["School (Class 8-10)", "College", "Competitive Exam", "Simple Hinglish"])
    if st.button("📚 Notes Banao", use_container_width=True):
        if topic:
            with st.spinner(f"{topic} ke notes bana raha hu..."):
                try:
                    r = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {"role":"system","content":f"You are best notes maker. Create beautiful, point-wise, easy notes. Use headings, bullet points, emojis. Language as per level {level}. Today {now.strftime('%d %B %Y')}"},
                            {"role":"user","content":f"Make detailed notes on {topic} for {level}"}
                        ]
                    )
                    st.markdown(r.choices[0].message.content)
                    st.download_button("⬇️ Notes Download Karo", r.choices[0].message.content, file_name=f"{topic}_notes.txt")
                except Exception as e:
                    st.error(str(e))
        else:
            st.warning("Topic to likho!")
