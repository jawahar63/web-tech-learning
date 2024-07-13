from flask import Flask, render_template, request, redirect, url_for, session
import os
import secrets

print("Flask application is running")
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Simulated user data
users = {
    "dav": {"password": "dav123", "balance": 1000},
    "user2": {"password": "password2", "balance": 500},
}

transactions = {
    "dav": [],
    "user2": [],
}

@app.route('/')
def index():
    print("Rendering index page")
    if 'username' in session:
        print(f"User {session['username']} is already logged in, redirecting to dashboard")
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    print("Login request received")
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)
    if user and user['password'] == password:
        print(f"User {username} logged in successfully")
        session['username'] = username
        return redirect(url_for('dashboard'))
    print("Login failed")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    print("Rendering dashboard page")
    if 'username' not in session:
        print("User is not logged in, redirecting to index")
        return redirect(url_for('index'))
    user = users.get(session['username'])
    if not user:
        print("User not found in database, redirecting to index")
        return redirect(url_for('index'))
    print(f"User {session['username']} has balance {user['balance']}")
    return render_template('dashboard.html', username=session['username'],
                           balance=user['balance'], transactions=transactions)

@app.route('/withdraw', methods=['POST'])
def withdraw():
    print("Withdraw request received")
    if 'username' not in session:
        print("User is not logged in, redirecting to index")
        return redirect(url_for('index'))
    amount = float(request.form['amount'])
    user = users.get(session['username'])
    if not user:
        print("User not found in database, redirecting to index")
        return redirect(url_for('index'))
    if amount <= 0 or user['balance'] < amount:
        print(f"Invalid withdrawal amount {amount} for user {session['username']}")
        return redirect(url_for('dashboard'))
    user['balance'] -= amount
    transactions[session['username']].append(f"Withdrawn {amount}, new balance: {user['balance']}")
    print(f"Withdrawn {amount} from user {session['username']}, new balance: {user['balance']}")
    return redirect(url_for('dashboard'))

@app.route('/deposit', methods=['POST'])
def deposit():
    print("Deposit request received")
    if 'username' not in session:
        print("User is not logged in, redirecting to index")
        return redirect(url_for('index'))
    amount = float(request.form['amount'])
    user = users.get(session['username'])
    if not user:
        print("User not found in database, redirecting to index")
        return redirect(url_for('index'))
    if amount <= 0:
        print(f"Invalid deposit amount {amount} for user {session['username']}")
        return redirect(url_for('dashboard'))
    user['balance'] += amount
    transactions[session['username']].append(f"Deposited {amount}, new balance: {user['balance']}")
    print(f"Deposited {amount} for user {session['username']}, new balance: {user['balance']}")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    print("Logout request received")
    username = session.pop('username', None)
    if username:
        print(f"User {username} logged out")
    else:
        print("No user was logged in")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
