from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


# INITIAL SETUP
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages and sessions

# Database configuration (SQLite)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "users.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy ORM
db = SQLAlchemy(app)


# DATABASE MODEL
class User(db.Model):
    """
    Represents a registered user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


# ROUTES
@app.route("/")
def home():
    """Redirects to the login page by default."""
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Handles user registration."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # Check if all fields are filled
        if not username or not email or not password or not confirm:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("register"))

        # Check password match
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.", "warning")
            return redirect(url_for("register"))

        # Hash the password and save user
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Find user in DB
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """User dashboard page (only accessible when logged in)."""
    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


@app.route("/logout")
def logout():
    """Logs the user out and clears the session."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# MAIN APP EXECUTION
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Automatically creates database and tables
    app.run(debug=True)
