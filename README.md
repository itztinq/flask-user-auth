# Information Security Lab 1 – User Authentication

A simple Flask web application demonstrating basic user registration, login, and authentication with secure password hashing.

### Features

- User registration with username, email, and password  
- Secure password hashing using Werkzeug  
- User login and session management  
- Dashboard accessible only to logged-in users  
- Flash messages for feedback  
- Logout functionality

### Setup 

1. Clone the repository:  
   `git clone https://github.com/yourusername/flask-user-auth.git`

2. Open the folder in your preferred code editor (e.g., VS Code).

3. Create and activate a virtual environment:  
   - **Windows:** `python -m venv venv` → `venv\Scripts\activate`  
   - **Mac/Linux:** `python -m venv venv` → `source venv/bin/activate`

4. Install dependencies:  
   `pip install -r requirements.txt`

5. Run the application:  
   `python app.py`

6. Open your browser at `http://127.0.0.1:5000` and test registration/login.
