
import csv
from collections import defaultdict


# --------------------------------------------------
# LOAD STUDENT DATA
# --------------------------------------------------

def load_student_data(file_path="data/student_academic_data.csv"):

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        records = []

        for row in reader:
            records.append({
                "student_id": row["student_id"],
                "student_name": row["student_name"],
                "department": row["department"],
                "semester": int(row["semester"]),
                "week": int(row["week"]),
                "subject": row["subject"],
                "attendance": float(row["attendance_percentage"]),
                "marks": float(row["internal_marks"]),
                "assignments_total": int(row["assignments_total"]),
                "assignments_submitted": int(
                    row["assignments_submitted"]
                )
            })

    return records


# --------------------------------------------------
# CALCULATE ACADEMIC TREND
# --------------------------------------------------

def calculate_trend(first_value, last_value):

    difference = last_value - first_value

    if difference < -5:
        return "Declining"

    elif difference > 5:
        return "Improving"

    return "Stable"


# --------------------------------------------------
# ANALYSE INDIVIDUAL STUDENT
# --------------------------------------------------

def analyse_student(records):

    reasons = []
    total_score = 0

    subject_groups = defaultdict(list)

    for record in records:
        subject_groups[record["subject"]].append(record)

    subject_results = []

    for subject, entries in subject_groups.items():

        entries.sort(key=lambda x: x["week"])

        attendance_values = [
            entry["attendance"] for entry in entries
        ]

        marks_values = [
            entry["marks"] for entry in entries
        ]

        attendance_average = (
            sum(attendance_values) / len(attendance_values)
        )

        marks_average = (
            sum(marks_values) / len(marks_values)
        )

        attendance_trend = calculate_trend(
            attendance_values[0],
            attendance_values[-1]
        )

        marks_trend = calculate_trend(
            marks_values[0],
            marks_values[-1]
        )

        total_assignments = sum(
            entry["assignments_total"] for entry in entries
        )

        submitted_assignments = sum(
            entry["assignments_submitted"] for entry in entries
        )

        missing_assignments = (
            total_assignments - submitted_assignments
        )

        # Attendance risk
        if attendance_average < 60:
            total_score += 35
            reasons.append(
                f"Very low attendance in {subject}"
            )

        elif attendance_average < 75:
            total_score += 20
            reasons.append(
                f"Attendance needs attention in {subject}"
            )

        elif attendance_trend == "Declining":
            total_score += 10
            reasons.append(
                f"Attendance is declining in {subject}"
            )

        # Internal marks risk
        if marks_average < 40:
            total_score += 30
            reasons.append(
                f"Low internal marks in {subject}"
            )

        elif marks_average < 50:
            total_score += 20
            reasons.append(
                f"Internal marks need improvement in {subject}"
            )

        elif marks_trend == "Declining":
            total_score += 10
            reasons.append(
                f"Marks are declining in {subject}"
            )

        # Assignment risk
        if missing_assignments >= 8:
            total_score += 35
            reasons.append(
                f"Many assignments are missing in {subject}"
            )

        elif missing_assignments >= 5:
            total_score += 20
            reasons.append(
                f"Several assignments are missing in {subject}"
            )

        elif missing_assignments >= 3:
            total_score += 10
            reasons.append(
                f"Some assignments are missing in {subject}"
            )

        subject_results.append({
            "subject": subject,
            "attendance_average": round(attendance_average, 2),
            "marks_average": round(marks_average, 2),
            "attendance_trend": attendance_trend,
            "marks_trend": marks_trend,
            "missing_assignments": missing_assignments
        })

    # Keep risk score between 0 and 100
    total_score = min(100, total_score)

    # Determine risk level
    if total_score >= 60:
        risk_level = "High"

    elif total_score >= 30:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    student = records[0]

    # Return both dashboard keys and original keys
    return {
        "student_id": student["student_id"],

        "name": student["student_name"],
        "dept": student["department"],
        "semester": student["semester"],
        "score": total_score,
        "level": risk_level,
        "reasons": reasons,

        # Original keys retained for compatibility
        "student_name": student["student_name"],
        "department": student["department"],
        "risk_score": total_score,
        "risk_level": risk_level,
        "risk_reasons": reasons,

        "subject_analysis": subject_results
    }


# --------------------------------------------------
# ANALYSE ALL STUDENTS
# --------------------------------------------------

def analyse_all_students():

    records = load_student_data()

    student_groups = defaultdict(list)

    for record in records:
        student_groups[record["student_id"]].append(record)

    results = []

    for student_records in student_groups.values():

        result = analyse_student(student_records)

        results.append(result)

    # Sort students by highest risk score
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


# --------------------------------------------------
# TEST THE RISK ANALYSIS AGENT
# --------------------------------------------------

if __name__ == "__main__":

    results = analyse_all_students()

    print("\nEARLYALERT RISK ANALYSIS")
    print("=" * 50)

    for student in results[:10]:

        print(
            student["student_id"],
            "|",
            student["student_name"],
            "| Score:",
            student["risk_score"],
            "| Risk:",
            student["risk_level"]
        )

        for reason in student["risk_reasons"][:3]:
            print("  -", reason)

    print("\nTotal students analysed:", len(results))
