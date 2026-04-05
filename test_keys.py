import google.generativeai as genai
from groq import Groq

# 1. Yahan apni keys direct likhein (Sirf test ke liye)
GEMINI_KEY="AIzaSyAr1KC0PKHUb1CorizTu7ptf8h8LdpS5mA"
GROQ_KEY="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"

print("--- Testing Gemini ---")
try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Hello")
    print("✅ Gemini Working! Response:", response.text)
except Exception as e:
    print("❌ Gemini Failed Error:", e)

print("\n--- Testing Groq ---")
try:
    client = Groq(api_key=GROQ_KEY)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello"}],
        model="llama-3.1-8b-instant",
    )
    print("✅ Groq Working! Response:", chat_completion.choices[0].message.content)
except Exception as e:
    print("❌ Groq Failed Error:", e)