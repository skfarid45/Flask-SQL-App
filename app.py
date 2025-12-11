import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        mysql.connection.commit()
        cur.close()

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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
