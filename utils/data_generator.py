
import csv
import random
import os

random.seed(42)

SUBJECTS = [
    "Mathematics",
    "Data Structures",
    "Database Management",
    "Operating Systems",
    "Computer Networks"
]

DEPARTMENTS = ["CSE", "ISE", "ECE", "AIML"]


def generate_student_dataset(num_students=100, weeks=8):

    records = []

    for i in range(1, num_students + 1):

        student_id = f"EA{i:03d}"
        student_name = f"Student {i:03d}"

        department = random.choice(DEPARTMENTS)
        semester = random.choice([3, 4, 5, 6])

        pattern = random.choices(
            ["stable", "declining", "improving"],
            weights=[50, 30, 20]
        )[0]

        base_attendance = random.randint(65, 96)
        base_marks = random.randint(45, 91)

        for week in range(1, weeks + 1):

            if pattern == "declining":
                attendance_change = -2.5 * (week - 1)
                marks_change = -2.0 * (week - 1)

            elif pattern == "improving":
                attendance_change = 2.0 * (week - 1)
                marks_change = 2.5 * (week - 1)

            else:
                attendance_change = 0
                marks_change = 0

            for subject in SUBJECTS:

                attendance = max(30, min(100,
                    base_attendance
                    + attendance_change
                    + random.gauss(0, 5)
                ))

                marks = max(0, min(100,
                    base_marks
                    + marks_change
                    + random.gauss(0, 7)
                ))

                submission_probability = max(
                    0.15,
                    0.90 - (
                        (week - 1) * 0.07
                        if pattern == "declining"
                        else 0
                    )
                )

                total_assignments = 2

                submitted = sum(
                    1 for _ in range(total_assignments)
                    if random.random() < submission_probability
                )

                records.append({
                    "student_id": student_id,
                    "student_name": student_name,
                    "department": department,
                    "semester": semester,
                    "week": week,
                    "subject": subject,
                    "attendance_percentage": round(attendance, 2),
                    "internal_marks": round(marks, 2),
                    "assignments_total": total_assignments,
                    "assignments_submitted": submitted,
                    "academic_pattern": pattern
                })

    return records


if __name__ == "__main__":

    data = generate_student_dataset()

    os.makedirs("data", exist_ok=True)

    file_path = os.path.join(
        "data",
        "student_academic_data.csv"
    )

    with open(file_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=data[0].keys()
        )

        writer.writeheader()
        writer.writerows(data)

    print("EarlyAlert dataset generated successfully!")
    print("Number of students:", len(set(
        row["student_id"] for row in data
    )))
    print("Number of records:", len(data))
    print("Number of weeks:", len(set(
        row["week"] for row in data
    )))
    print("Number of subjects:", len(SUBJECTS))
    print("Saved to:", file_path)
