from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create a context manager for your app
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# Routes and other code for registration and login go here

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# Import the render_template function
from flask import render_template

# ... (Your existing code for app configuration and database setup)

# Routes and other code for registration and login go here

@app.route('/')
def home():
    return 'Welcome to the Bus Booking App'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve user input and create a new user record in the database
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return 'Registration successful'  # You can redirect to a login page if desired

    # Render the 'register.html' template for GET requests
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve user input and check credentials
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return 'Login successful'  # Implement session management or token-based auth
        else:
            return 'Login failed'

    # Render the 'login.html' template for GET requests
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
