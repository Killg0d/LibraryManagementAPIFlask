from flask import jsonify, request
from db.database import initialize_db, get_db_connection
from utils.auth import authenticate_user, generate_token, save_session
from app_factory import create_app


app = create_app()

@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and generate a session token."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    # Authenticate the user
    user_id = authenticate_user(username, password)
    if user_id is None:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Generate and save the session token
    token = generate_token(username)
    save_session(user_id, token)
    
    return jsonify({"message": "Login successful", "token": token}), 200
