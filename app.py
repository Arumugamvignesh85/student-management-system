from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        student_id = request.form['id']
        name = request.form['name']
        department = request.form['department']
        marks = request.form['marks']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students VALUES(?,?,?,?)",
            (student_id, name, department, marks)
        )

        conn.commit()
        conn.close()

        return "Student Added Successfully"

    return render_template('add_student.html')

@app.route('/students')
def view_students():

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'view_students.html',
        students=students
    )
@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect('students.db')

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    return "Student Deleted Successfully"
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        department = request.form['department']
        marks = request.form['marks']

        cursor.execute(
            "UPDATE students SET name=?, department=?, marks=? WHERE id=?",
            (name, department, marks, id)
        )

        conn.commit()
        conn.close()

        return "Student Updated Successfully"

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_student.html',
        student=student
    )

if __name__ == '__main__':
    app.run(debug=True)