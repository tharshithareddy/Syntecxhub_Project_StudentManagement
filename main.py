import json
from pathlib import Path

# The data file is stored in the same folder as this Python program.
DATA_FILE = Path(__file__).with_name("students.json")


class Student:
    """Represents one student."""

    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        """Convert a Student object into a dictionary for JSON storage."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "grade": self.grade,
        }


class StudentManager:
    """Adds, updates, deletes, lists, loads, and saves student records."""

    def __init__(self):
        self.students = {}
        self.load_students()

    def load_students(self):
        """Load student records from the JSON file, if it exists."""
        if not DATA_FILE.exists():
            return

        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                records = json.load(file)

            if not isinstance(records, list):
                raise ValueError("The JSON file must contain a list of students.")

            loaded = {}
            for record in records:
                student_id = str(record["student_id"]).strip()
                name = str(record["name"]).strip()
                grade = str(record["grade"]).strip()

                if not student_id or not name or not grade:
                    raise ValueError("A saved student has a missing field.")
                if student_id in loaded:
                    raise ValueError(f"Duplicate student ID in saved data: {student_id}")

                loaded[student_id] = Student(student_id, name, grade)

            self.students = loaded

        except (OSError, json.JSONDecodeError, ValueError, KeyError, TypeError) as error:
            print(f"Could not load student data: {error}")
            print("Please check students.json and run the program again.")
            raise SystemExit(1)

    def save_students(self):
        """Save all current student records to the JSON file."""
        records = [student.to_dict() for student in self.students.values()]
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

    def add_student(self):
        student_id = input("Enter student ID: ").strip()

        if not student_id:
            print("Student ID cannot be empty.")
            return
        if student_id in self.students:
            print("Error: This student ID already exists.")
            return

        name = input("Enter student name: ").strip()
        grade = input("Enter student grade: ").strip()

        if not name or not grade:
            print("Name and grade cannot be empty.")
            return

        self.students[student_id] = Student(student_id, name, grade)
        try:
            self.save_students()
        except OSError as error:
            del self.students[student_id]
            print(f"Could not save student data: {error}")
            return

        print("Student added successfully!")

    def update_student(self):
        student_id = input("Enter student ID to update: ").strip()
        student = self.students.get(student_id)

        if student is None:
            print("Student not found.")
            return

        new_name = input(f"Enter new name [{student.name}] (press Enter to keep): ").strip()
        new_grade = input(f"Enter new grade [{student.grade}] (press Enter to keep): ").strip()

        old_name, old_grade = student.name, student.grade
        if new_name:
            student.name = new_name
        if new_grade:
            student.grade = new_grade

        try:
            self.save_students()
        except OSError as error:
            student.name, student.grade = old_name, old_grade
            print(f"Could not save changes: {error}")
            return

        print("Student updated successfully!")

    def delete_student(self):
        student_id = input("Enter student ID to delete: ").strip()
        student = self.students.get(student_id)

        if student is None:
            print("Student not found.")
            return

        confirm = input(f"Delete {student.name} (ID: {student_id})? (y/n): ").strip().lower()
        if confirm != "y":
            print("Deletion cancelled.")
            return

        del self.students[student_id]
        try:
            self.save_students()
        except OSError as error:
            self.students[student_id] = student
            print(f"Could not save deletion: {error}")
            return

        print("Student deleted successfully!")

    def list_students(self):
        if not self.students:
            print("No student records available.")
            return

        print()
        print("-" * 62)
        print(f"{'STUDENT ID':<16}{'NAME':<30}{'GRADE':<16}")
        print("-" * 62)
        for student_id in sorted(self.students):
            student = self.students[student_id]
            print(f"{student.student_id:<16}{student.name:<30}{student.grade:<16}")
        print("-" * 62)
        print(f"Total students: {len(self.students)}")

    def run(self):
        while True:
            print("\n===== STUDENT MANAGEMENT SYSTEM =====")
            print("1. Add Student")
            print("2. Update Student")
            print("3. Delete Student")
            print("4. List Students")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ").strip()

            try:
                if choice == "1":
                    self.add_student()
                elif choice == "2":
                    self.update_student()
                elif choice == "3":
                    self.delete_student()
                elif choice == "4":
                    self.list_students()
                elif choice == "5":
                    print("Thank you for using the Student Management System!")
                    break
                else:
                    print("Invalid choice. Please enter a number from 1 to 5.")
            except OSError as error:
                print(f"File error: {error}")


def main():
    manager = StudentManager()
    manager.run()


if __name__ == "__main__":
    main()
