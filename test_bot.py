import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. .env file se chupke se chabi (key) nikalna
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

# 2. Gemini ko chabi dena taaki wo connect ho sake
genai.configure(api_key=gemini_key)

# 3. Model select karna (Hum fast 'flash' model use kar rahe hain)
model = genai.GenerativeModel('gemini-2.5-flash')

print("🤖 Gemini se connect ho raha hai... Please wait...\n")

# 4. Gemini se apna pehla sawal poochna
response = model.generate_content("Namaste! Main VS Code mein apna pehla AI app bana raha hoon. Mujhe ek chhoti si aur joshili greeting do!")

# 5. Gemini ka jawab screen par dikhana
print("✨ Gemini ka Jawab:")
print(response.text)