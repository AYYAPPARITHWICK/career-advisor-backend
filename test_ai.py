import os
import google.generativeai as genai

API_KEY = os.environ.get("GOOGLE_API_KEY")
print("GOOGLE_API_KEY:", API_KEY)

genai.configure(api_key=API_KEY)

try:
    response = genai.chat.create(
        model="gemini-1.5-t",
        messages=[{"author": "user", "content": "I want to become a cloud architect"}]
    )
    print(response.text)
except Exception as e:
    print("AI error:", e)
