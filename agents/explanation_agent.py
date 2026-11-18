
import streamlit as st
from groq import Groq


def generate_explanation(student):
    """
    Uses Groq AI to explain a student's academic risk
    based on the results produced by the risk agent.
    """

    try:
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)

        student_id = student.get("student_id", "Unknown")
        risk_level = student.get("level", "Unknown")
        risk_score = student.get("score", 0)
        reasons = student.get("reasons", [])
        subject_analysis = student.get("subject_analysis", {})

        prompt = f"""
You are an Academic Support Assistant for the EarlyAlert system.

Your job is to explain academic risk to a college mentor.

Analyse only the information provided below.

STUDENT ACADEMIC INFORMATION:

Student ID: {student_id}
Risk Level: {risk_level}
Risk Score: {risk_score}/100

Risk Factors:
{reasons}

Subject-wise Analysis:
{subject_analysis}

Prepare your explanation using these sections:

1. Risk Summary
Explain the student's current academic risk in simple language.

2. Main Reasons
Explain the specific factors contributing to the risk.
Mention relevant subjects wherever possible.

3. Recommended Support Actions
Suggest 3 practical actions a mentor can take to help the student.

4. Mentor Observation
Write one short observation that a mentor should keep in mind.

IMPORTANT RULES:
- Use simple, clear language.
- Do not invent information.
- Do not assume reasons that are not present in the data.
- Treat the risk level as an early-warning indicator, not a permanent label.
- Be supportive and constructive.
- Do not shame or judge the student.
- If information is missing, clearly say it is unavailable.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful academic support assistant. "
                        "Provide evidence-based and supportive explanations."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_completion_tokens=1000
        )

        explanation = response.choices[0].message.content

        return explanation

    except Exception as error:
        return f"Unable to generate AI explanation. Error: {error}"
