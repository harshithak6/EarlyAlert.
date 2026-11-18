
import csv
from collections import defaultdict


def load_historical_data(
    file_path="data/student_academic_data.csv"
):
    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append({
                "student_id": row["student_id"],
                "student_name": row["student_name"],
                "week": int(row["week"]),
                "subject": row["subject"],
                "attendance": float(
                    row["attendance_percentage"]
                ),
                "marks": float(row["internal_marks"]),
                "assignments_total": int(
                    row["assignments_total"]
                ),
                "assignments_submitted": int(
                    row["assignments_submitted"]
                )
            })

    return records


def generate_historical_report(student_id):

    records = load_historical_data()

    student_records = [
        record for record in records
        if record["student_id"] == student_id
    ]

    if not student_records:
        return None

    weekly_data = defaultdict(list)

    for record in student_records:
        weekly_data[record["week"]].append(record)

    report = []

    for week, entries in sorted(weekly_data.items()):

        total_attendance = sum(
            entry["attendance"] for entry in entries
        )

        total_marks = sum(
            entry["marks"] for entry in entries
        )

        total_assignments = sum(
            entry["assignments_total"] for entry in entries
        )

        submitted_assignments = sum(
            entry["assignments_submitted"] for entry in entries
        )

        subject_count = len(entries)

        attendance_average = (
            total_attendance / subject_count
        )

        marks_average = (
            total_marks / subject_count
        )

        missing_assignments = (
            total_assignments - submitted_assignments
        )

        submission_percentage = (
            submitted_assignments / total_assignments * 100
            if total_assignments > 0 else 0
        )

        # Simplified weekly risk indicator
        weekly_risk_score = 0

        if attendance_average < 60:
            weekly_risk_score += 35
        elif attendance_average < 75:
            weekly_risk_score += 20

        if marks_average < 40:
            weekly_risk_score += 30
        elif marks_average < 50:
            weekly_risk_score += 20

        if missing_assignments >= 8:
            weekly_risk_score += 35
        elif missing_assignments >= 5:
            weekly_risk_score += 20
        elif missing_assignments >= 3:
            weekly_risk_score += 10

        weekly_risk_score = min(100, weekly_risk_score)

        if weekly_risk_score >= 60:
            weekly_risk_level = "High"
        elif weekly_risk_score >= 30:
            weekly_risk_level = "Medium"
        else:
            weekly_risk_level = "Low"

        report.append({
            "week": week,
            "attendance": round(attendance_average, 2),
            "marks": round(marks_average, 2),
            "assignments_submitted": submitted_assignments,
            "assignments_total": total_assignments,
            "submission_percentage": round(
                submission_percentage, 2
            ),
            "missing_assignments": missing_assignments,
            "risk_score": weekly_risk_score,
            "risk_level": weekly_risk_level
        })

    return report


def generate_progress_summary(report):

    if not report:
        return "No historical records available."

    first_week = report[0]
    latest_week = report[-1]

    attendance_change = (
        latest_week["attendance"] - first_week["attendance"]
    )

    marks_change = (
        latest_week["marks"] - first_week["marks"]
    )

    if attendance_change > 0:
        attendance_status = "Attendance improved"
    elif attendance_change < 0:
        attendance_status = "Attendance declined"
    else:
        attendance_status = "Attendance remained stable"

    if marks_change > 0:
        marks_status = "Internal marks improved"
    elif marks_change < 0:
        marks_status = "Internal marks declined"
    else:
        marks_status = "Internal marks remained stable"

    return {
        "attendance_change": round(attendance_change, 2),
        "marks_change": round(marks_change, 2),
        "attendance_status": attendance_status,
        "marks_status": marks_status,
        "latest_risk": latest_week["risk_level"]
    }


# TEST HISTORY AGENT

if __name__ == "__main__":

    report = generate_historical_report("EA001")

    if report:

        print("\nEARLYALERT HISTORICAL REPORT")
        print("=" * 45)

        for week in report:

            print(
                f"Week {week['week']} | "
                f"Attendance: {week['attendance']}% | "
                f"Marks: {week['marks']} | "
                f"Assignments: "
                f"{week['assignments_submitted']}/"
                f"{week['assignments_total']} | "
                f"Risk: {week['risk_level']}"
            )

        print("\nPROGRESS SUMMARY")

        summary = generate_progress_summary(report)

        print(summary)

    else:
        print("Student records not found.")
