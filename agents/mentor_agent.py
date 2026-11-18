
from datetime import datetime, timedelta


def generate_mentor_note(student, explanation):
    """
    Creates a personalised mentor communication draft.
    The message is not sent automatically.
    """

    name = student.get("name", "Student")
    student_id = student.get("student_id", "Unknown")
    risk_level = student.get("level", "Unknown")
    risk_score = student.get("score", 0)
    reasons = student.get("reasons", [])

    reason_text = "\n".join(
        f"- {reason}" for reason in reasons
    ) if reasons else "- No major risk factors detected."

    # Suggest a meeting slot for the next working day.
    proposed_meeting = (
        datetime.now() + timedelta(days=1)
    ).replace(hour=11, minute=0, second=0, microsecond=0)

    meeting_text = proposed_meeting.strftime(
        "%d %B %Y at %I:%M %p"
    )

    message = f"""
Subject: Academic Support Meeting – {student_id}

Dear Mentor,

I would like to bring the following student to your attention
for a supportive academic check-in.

Student Name: {name}
Student ID: {student_id}
Risk Level: {risk_level}
Risk Score: {risk_score}/100

Observed Academic Concerns:
{reason_text}

AI-Generated Academic Explanation:
{explanation}

Suggested Mentor Actions:
1. Discuss the student's current academic challenges.
2. Review attendance and pending assignments.
3. Create a realistic academic improvement plan.
4. Monitor progress during the coming weeks.

Proposed Meeting Slot:
{meeting_text}

Please review this draft and make any necessary changes
before contacting the student.

Regards,
EarlyAlert Academic Support System
"""

    return {
        "student_id": student_id,
        "meeting_slot": meeting_text,
        "message": message
    }
