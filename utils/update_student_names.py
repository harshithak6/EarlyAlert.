
import csv

CSV_FILE = "data/student_academic_data.csv"

first_names = [
    "Aarav", "Ananya", "Rahul", "Sneha", "Arjun",
    "Priya", "Rohan", "Kavya", "Aditya", "Meera"
]

last_names = [
    "Sharma", "Reddy", "Kumar", "Patel", "Verma",
    "Singh", "Nair", "Gupta", "Rao", "Iyer"
]

# Generate 100 unique fictional names
names = [
    f"{first_names[i // 10]} {last_names[i % 10]}"
    for i in range(100)
]

# Map each student ID to a name
student_names = {
    f"EA{i + 1:03d}": names[i]
    for i in range(100)
}

# Read existing CSV data
with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames
    rows = list(reader)

# Update only the student_name column
for row in rows:
    student_id = row["student_id"]
    if student_id in student_names:
        row["student_name"] = student_names[student_id]

# Save the updated CSV
with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Successfully updated student names!")
print("Total fictional names:", len(student_names))
print("Sample updated names:")

for student_id in list(student_names.keys())[:10]:
    print(student_id, "->", student_names[student_id])
