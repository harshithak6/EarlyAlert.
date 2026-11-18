
import streamlit as st
from groq import Groq

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)

    print("Connecting to Groq...")

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": "Say: EarlyAlert Groq connection successful!"
            }
        ],
        temperature=0.2,
        max_tokens=100,
    )

    print("\nSUCCESS! Groq is connected.")
    print(response.choices[0].message.content)

except Exception as error:
    print("\nGroq connection failed.")
    print("Error:", error)
