from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       age INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Home page - Read all users
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

# Create a new user
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    age = request.form['age']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Update a user
@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    age = request.form['age']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Delete a user
@app.route('/delete/<int:id>')
def delete_user(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)