from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os
import threading

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'student.db')

# Function to get database connection for the current thread
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        # Create students table if it doesn't exist
        with db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade INTEGER NOT NULL
                )
            ''')
    return db

# Function to close database connection when app context is torn down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route for adding a student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        db = get_db()
        with db:
            db.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
        return redirect(url_for('admin_view'))
    return render_template('add_student.html')

# Route for admin panel
@app.route('/admin')
def admin_view():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    return render_template('admin.html', students=students)

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
