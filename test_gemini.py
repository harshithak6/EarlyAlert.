
import streamlit as st
from google import genai

try:
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(api_key=api_key)

    print("Connecting to Gemini...")

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input="Say: EarlyAlert Gemini connection successful!"
    )

    print("\nSUCCESS! Gemini is connected.")
    print(response.output_text)

except Exception as error:
    print("\nGemini connection failed.")
    print("Error:", error)
