import os
from flask import Flask, render_template, request, jsonify
import pymysql
pymysql.install_as_MySQLdb()      # <-- Required for Windows
from flask_mysqldb import MySQL

app = Flask(__name__)

# -------------------------------
# MySQL CONFIG (LOCAL TESTING)
# -------------------------------
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'devops')

mysql = MySQL(app)

# -------------------------------
# INITIALIZE DB TABLE
# -------------------------------
def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        mysql.connection.commit()
        cur.close()

# -------------------------------
# ROUTES
# -------------------------------

@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages')
def get_messages():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, message, DATE_FORMAT(created_at, '%H:%i %d-%m-%Y') FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    cur.close()
    return jsonify(messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (message) VALUES (%s)", [new_message])
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": new_message})

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_message(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM messages WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    return jsonify({"deleted": id})

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)