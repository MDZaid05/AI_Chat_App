import streamlit as st
import os
import json
import tempfile
import google.generativeai as genai
from groq import Groq

# 1. Apni Sahi Keys Yahan Daalein
GEMINI_KEY="AIzaSyAr1KC0PKHUb1CorizTu7ptf8h8LdpS5mA"
GROQ_KEY="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"
# 2. AI Setup
genai.configure(api_key=GEMINI_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# -----------------------------------------------------
# MEMORY POWER 
# -----------------------------------------------------
MEMORY_FILE = "zaid_chat_history.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return []

def save_memory(messages):
    with open(MEMORY_FILE, "w") as file:
        json.dump(messages, file)
# -----------------------------------------------------

st.set_page_config(page_title="Dual-Core LLM Engine", layout="wide")

st.title("🧠 Dual-Core LLM Engine")
st.write("Powered by Gemini Vision & Groq Llama 3.1 | Intelligent Routing System")

# Memory load karna
if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

# -----------------------------------------------------
# SIDEBAR: UPLOAD FILE & SETTINGS
# -----------------------------------------------------
with st.sidebar:
    st.header("📎 File Upload Karein")
    
    # NAYA FEATURE: Kisi bhi file ko upload karne ka dabba
    uploaded_file = st.file_uploader("Yahan Photo, PDF ya Video daalein", type=["jpg", "jpeg", "png", "pdf", "mp4"])
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} ready hai! Ab apna sawal poochiye.")
        
    st.markdown("---")
    st.header("⚙️ Settings")
    
    # Chat Download
    chat_text = ""
    for m in st.session_state.messages:
        role = "Zaid" if m["role"] == "user" else "AI"
        chat_text += f"{role}: {m['content']}\n\n"
        
    st.download_button("💾 Chat Download Karein", data=chat_text, file_name="Zaid_AI_Chat.txt", mime="text/plain")
    
    # Memory Delete
    if st.button("🗑️ Chat Memory Delete Karein"):
        st.session_state.messages = []
        save_memory([])
        st.rerun()

# -----------------------------------------------------
# MAIN CHAT SYSTEM
# -----------------------------------------------------
# Purane messages dikhana
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
user_input = st.chat_input("Yahan apna sawal likhein (ya file ke baare mein poocho)...")

if user_input:
    # User ka sawal memory mein add karna
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("ai"):
        with st.spinner("AI process kar raha hai... 🧠"):
            
            # SCENARIO 1: Agar User ne koi FILE UPLOAD ki hai
            if uploaded_file:
                try:
                    # File ko temporary save karna taaki AI padh sake
                    with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as temp_file:
                        temp_file.write(uploaded_file.getvalue())
                        temp_file_path = temp_file.name
                    
                    st.info("Gemini aapki file ko scan kar raha hai...")
                    
                    # Gemini ko file bhejna
                    gemini_uploaded = genai.upload_file(temp_file_path)
                    
                    # Gemini se jawab lena
                    response = gemini_model.generate_content([user_input, gemini_uploaded])
                    final_response = f"*(File mode: Yeh jawab sirf Gemini ne file padh kar diya hai)*\n\n{response.text}"
                    
                    # Temp file delete karna (Memory bachane ke liye)
                    os.remove(temp_file_path)
                except Exception as e:
                    final_response = f"❌ File padhne mein error aaya: {e}"
                    
            # SCENARIO 2: Agar User ne sirf TEXT type kiya hai (No File)
            else:
                try:
                    gemini_ans = gemini_model.generate_content(user_input).text
                except:
                    gemini_ans = "Gemini Busy"

                try:
                    groq_resp = groq_client.chat.completions.create(
                        model="llama-3.1-8b-instant",  
                        messages=[{"role": "user", "content": user_input}]
                    )
                    groq_ans = groq_resp.choices[0].message.content
                except:
                    groq_ans = "Groq Error"

                if "Error" in groq_ans and "Busy" in gemini_ans:
                    final_response = "Dono AI thak gaye hain. 1 minute baad try karein!"
                elif "Busy" in gemini_ans:
                    final_response = f"*(Groq Llama 3.1)*\n\n{groq_ans}"
                elif "Error" in groq_ans:
                    final_response = gemini_ans
                else:
                    try:
                        judge_prompt = f"Sawal: {user_input}\nJawab 1: {gemini_ans}\nJawab 2: {groq_ans}\nIn dono ko mila kar ek aasan jawab do."
                        final_response = gemini_model.generate_content(judge_prompt).text
                    except:
                        final_response = groq_ans 

            st.write(final_response)
        
    # AI ka jawab memory mein add karke Save karna
    st.session_state.messages.append({"role": "ai", "content": final_response})
    save_memory(st.session_state.messages)