# app.py
from flask import Flask, render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/internhub'
mongo = PyMongo(app)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            return render_template('signup.html', error="❌ User already exists.")

        mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'password': password
        })
        return redirect('/login')

    return render_template('signup.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        user = mongo.db.users.find_one({'email': email})

        if user and user['password'] == password:
            session['user'] = user['name']  # storing name
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='❌ Invalid email or password.')

    return render_template('login.html')


# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    user = {'name': session['user']}
    referral_link = f'https://internhub.com/referral/{session["user"].lower().replace(" ", "")}123'
    return render_template('dashboard.html', user=user, referral_link=referral_link)





# Leaderboard Route
@app.route('/leaderboard')
def leaderboard():
    users = list(mongo.db.users.find())
    return render_template('leaderboard.html', users=users)

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))  # or homepage


if __name__ == '__main__':
    app.run(debug=True)

