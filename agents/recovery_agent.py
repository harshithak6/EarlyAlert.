
# --------------------------------------------------
# EARLYALERT - RECOVERY PLANNING AGENT
# --------------------------------------------------

def calculate_projected_risk(
    student,
    attendance_target=85,
    marks_improvement=10,
    complete_missing=False
):

    original_score = student["score"]

    projected_score = 0

    projected_subjects = []

    # Analyse each subject
    for subject in student["subject_analysis"]:

        current_attendance = subject["attendance_average"]
        current_marks = subject["marks_average"]
        current_missing = subject["missing_assignments"]

        # Project improved attendance
        projected_attendance = max(
            current_attendance,
            attendance_target
        )

        projected_attendance = min(
            100,
            projected_attendance
        )

        # Project improved internal marks
        projected_marks = min(
            100,
            current_marks + marks_improvement
        )

        # Project assignment completion
        if complete_missing:
            projected_missing = 0
        else:
            projected_missing = current_missing

        # Calculate attendance risk
        if projected_attendance < 60:
            projected_score += 35

        elif projected_attendance < 75:
            projected_score += 20

        # Calculate marks risk
        if projected_marks < 40:
            projected_score += 30

        elif projected_marks < 50:
            projected_score += 20

        # Calculate assignment risk
        if projected_missing >= 8:
            projected_score += 35

        elif projected_missing >= 5:
            projected_score += 20

        elif projected_missing >= 3:
            projected_score += 10

        # Store projected subject details
        projected_subjects.append({

            "subject": subject["subject"],

            "projected_attendance": round(
                projected_attendance, 2
            ),

            "projected_marks": round(
                projected_marks, 2
            ),

            "projected_missing_assignments": projected_missing

        })

    # Keep projected score between 0 and 100
    projected_score = min(100, projected_score)

    # Determine projected risk level
    if projected_score >= 60:
        projected_level = "High"

    elif projected_score >= 30:
        projected_level = "Medium"

    else:
        projected_level = "Low"

    # Calculate risk score reduction
    score_reduction = original_score - projected_score

    # Return results to dashboard
    return {

        "original_score": original_score,

        "projected_score": projected_score,

        "projected_level": projected_level,

        "score_reduction": score_reduction,

        "projected_subjects": projected_subjects

    }


# --------------------------------------------------
# TEST RECOVERY AGENT
# --------------------------------------------------

if __name__ == "__main__":

    from agents.risk_agent import analyse_all_students

    students = analyse_all_students()

    if students:

        student = students[0]

        result = calculate_projected_risk(
            student,
            attendance_target=85,
            marks_improvement=10,
            complete_missing=True
        )

        print("\nEARLYALERT RECOVERY SIMULATOR")
        print("=" * 40)

        print("Student:", student["name"])

        print("Original Score:", result["original_score"])

        print("Projected Score:", result["projected_score"])

        print("Projected Risk:", result["projected_level"])

        print("Score Reduction:", result["score_reduction"])

        print("\nSubject-wise Improvements:")

        for subject in result["projected_subjects"]:

            print("\nSubject:", subject["subject"])

            print(
                "Attendance:",
                subject["projected_attendance"]
            )

            print(
                "Marks:",
                subject["projected_marks"]
            )

            print(
                "Missing Assignments:",
                subject["projected_missing_assignments"]
            )
