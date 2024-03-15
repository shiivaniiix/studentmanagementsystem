# studentmanagementsystem
Student Management System using python and sqlite 
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

# Create a table to store student information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        grade INTEGER
    )
''')
conn.commit()


def admin_menu():
    print("\nAdmin Menu:")
    print("1. Add Student")
    print("2. Update Student")
    print("3. Delete Student")
    print("4. View Students")
    print("5. Logout")


def teacher_menu():
    print("\nTeacher Menu:")
    print("1. Update Student")
    print("2. View Students")
    print("3. Logout")


def student_menu():
    print("\nStudent Menu:")
    print("1. View Students")
    print("2. Logout")


def add_student():
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    grade = int(input("Enter student grade: "))
    cursor.execute('''
        INSERT INTO students (name, age, grade)
        VALUES (?, ?, ?)
    ''', (name, age, grade))
    conn.commit()
    print("Student added successfully.")


def update_student():
    student_id = int(input("Enter student ID to update: "))
    name = input("Enter new name (press enter to keep old name): ")
    age = input("Enter new age (press enter to keep old age): ")
    grade = input("Enter new grade (press enter to keep old grade): ")

    update_query = "UPDATE students SET"
    if name:
        update_query += f" name = '{name}',"
    if age:
        update_query += f" age = {age},"
    if grade:
        update_query += f" grade = {grade},"

    update_query = update_query.rstrip(',') + f" WHERE id = {student_id}"
    cursor.execute(update_query)
    conn.commit()
    print("Student updated successfully.")


def delete_student():
    student_id = int(input("Enter student ID to delete: "))
    cursor.execute('''
        DELETE FROM students WHERE id = ?
    ''', (student_id,))
    conn.commit()
    print("Student deleted successfully.")


def view_students():
    cursor.execute('''
        SELECT * FROM students
    ''')
    students = cursor.fetchall()
    print("\nStudent ID\tName\tAge\tGrade")
    for student in students:
        print(f"{student[0]}\t\t{student[1]}\t{student[2]}\t{student[3]}")


def login():
    while True:
        user_type = input("\nChoose user type (admin/teacher/student): ").lower()
        if user_type not in ['admin', 'teacher', 'student']:
            print("Invalid user type. Please choose again.")
            continue

        return user_type


def main():
    while True:
        user_type = login()
        if user_type == 'admin':
            while True:
                admin_menu()
                choice = input("Enter your choice: ")
                if choice == '1':
                    add_student()
                elif choice == '2':
                    update_student()
                elif choice == '3':
                    delete_student()
                elif choice == '4':
                    view_students()
                elif choice == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif user_type == 'teacher':
            while True:
                teacher_menu()
                choice = input("Enter your choice: ")
                if choice == '1':
                    update_student()
                elif choice == '2':
                    view_students()
                elif choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif user_type == 'student':
            while True:
                student_menu()
                choice = input("Enter your choice: ")
                if choice == '1':
                    view_students()
                elif choice == '2':
                    break
                else:
                    print("Invalid choice. Please try again.")

        logout = input("\nDo you want to logout? (yes/no): ").lower()
        if logout == 'yes':
            break


if __name__ == "__main__":
    main()

# Close the connection to the SQLite database
conn.close()
