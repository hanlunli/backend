from flask import Flask, render_template, flash, request, redirect, jsonify
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from forms import LoginForm
from flask_cors import CORS
import os

app = Flask(__name__)
app.debug = True

# Allow CORS from any origin
CORS(app, resources={r"/messageDB": {"origins": "*"}})

login_manager = LoginManager(app)
login_manager.login_view = "login"
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class User(UserMixin):
    def __init__(self, id, username, password, email):
        self.id = str(id)
        self.username = username
        self.password = password
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('login.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM login WHERE user_id = ?", [user_id])
    lu = curs.fetchone()
    conn.close()
    if lu is None:
        return None
    else:
        return User(int(lu[0]), lu[1], lu[3], lu[2])

# ... your existing Flask
# add an api endpoint to flask app
def init_db():
    conn = sqlite3.connect('message.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Function to add a message to the database
def add_message(message):
    conn = sqlite3.connect('message.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (message) VALUES (?)', (message,))
    conn.commit()
    conn.close()

# Function to get the latest message from the database
def get_latest_message():
    conn = sqlite3.connect('message.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM messages ORDER BY id DESC')
    message = cursor.fetchall()
    conn.close()
    return message[0] if message else ""

def clear_db():
    # if request.method == 'POST':
        # Provide a secret key or some form of authentication/authorization to prevent unauthorized access

        # Clear the SQLite database
    try:
        conn = sqlite3.connect('message.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages')
        conn.commit()
        conn.close()
        return "Database cleared successfully", 200
    except Exception as e:
        return "An error occurred while clearing the database", 500

@app.route('/clear_db', methods=['GET', 'POST'])
def get_clear_db():
    clear_db()

        
# Add an API endpoint to the Flask app
@app.route('/messageDB', methods=["POST", "GET"])
def messageDB():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if "message" in data:
                message = data["message"]
                add_message(message)  # Store the message in the database

                response_data = {"message": "Message received and stored successfully"}
                return jsonify(response_data), 200
            else:
                return jsonify({"error": "Invalid request format"}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred during message processing"}), 500

    elif request.method == 'GET':
        conn = sqlite3.connect('message.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages')
        messages = cursor.fetchall()
        conn.close()

        # Convert the result to a list of dictionaries for easy JSON serialization
        messages_list = {int(message[0]): message[1] for message in messages}
        
        return jsonify(messages_list)

@app.route('/messageDB/all', methods=["GET"])
def all_messages():
    conn = sqlite3.connect('message.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages')
    messages = cursor.fetchall()
    conn.close()

    # Convert the result to a list of dictionaries for easy JSON serialization
    messages_list = [{"id": message[0], "message": message[1]} for message in messages]
    
    return jsonify(messages_list)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/userDic", methods=['GET', 'POST'])
def userDic():
    connection = sqlite3.connect("login.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM login")
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    result = [dict(zip(column_names, row)) for row in data]
    connection.close()

    return(result)

@app.route("/registerAcc", methods=['GET', 'POST'])
def registerAcc():
    try:
        userEmail = request.form['email']
        userPassword = request.form['password']
        userName = request.form['username']

        addDB = "INSERT INTO login (username, email, password) VALUES (?, ?, ?)"
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        cursor.execute(addDB, (userName, userEmail, userPassword))
        conn.commit()
        conn.close()

        return redirect("/login")
    except Exception as e:
        # Handle the exception, e.g., log the error or return an error page
        return "An error occurred during registration."

@app.route("/login", methods=['POST'])
def login():
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    if current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Already logged in'})

    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('login.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM login WHERE username = ?", [form.username.data])
        user = curs.fetchone()
        conn.close()

        if user:
            if form.username.data == user[1] and form.password.data == user[3]:
                Us = load_user(user[0])
                login_user(Us, remember=form.remember.data)
                flash('Logged in successfully ' + form.username.data)
                return jsonify({'success': True, 'message': 'Login successful'})
            else:
                return jsonify({'success': False, 'message': 'Incorrect password'})
        else:
            return jsonify({'success': False, 'message': 'User not found'})

    return jsonify({'success': False, 'message': 'Invalid form data' 'Data': username})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True)
