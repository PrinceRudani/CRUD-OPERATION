
from flask import Flask, session, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/login', methods=['POST'])
def login():
    session['user_id'] = 1  # Store session in server
    return "User logged in"

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' in session:
        return "Welcome to dashboard"
    return "Unauthorized", 401
