#imports for the auth
from flask import Flask, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import db, NutritionLog
import os
from dotenv import load_dotenv
from flask_cors import CORS
import uuid  # Add this import at the top of your file

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Create auth blueprint
auth = Blueprint('auth', __name__)

# JWT secret key from environment variable
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

#create a token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if 'Authorization' in request.headers:
            print("Authorization Header:", request.headers['Authorization'])  # Debugging log
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = NutritionLog.query.filter_by(user_id=data['user_id']).first()
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'message': 'Invalid token!', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)
    return decorated

#create a register route
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get the JSON data from the request
    print("Received data:", data)  # Debugging log

    # Validate required fields
    required_fields = ['email', 'password', 'height', 'weight']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required!'}), 400

    # Check if the email is already registered
    if NutritionLog.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered!'}), 400

    # Generate a unique user_id
    user_id = str(uuid.uuid4())

    # Create a new user
    new_user = NutritionLog(
        user_id=user_id,  # Generate a unique user_id
        email=data['email'],
        password=generate_password_hash(data['password']),
        gender=data.get('gender'),  # Optional
        age=data.get('age'),  # Optional
        weight=data['weight'],
        height=data['height'],
        activity_level=data.get('activity_level'),  # Optional
        fat_logs=[],
        protein_logs=[],
        carbs_logs=[],
        cal_in_logs=[],
        cal_out_logs=[]
    )

    # Add the new user to the database
    try:
        db.session.add(new_user)
        db.session.commit()

        # Generate a token for the new user
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, JWT_SECRET_KEY, algorithm="HS256")

        return jsonify({
            'message': 'User registered successfully!',
            'user_id': user_id,
            'token': token  # Include the token in the response
        }), 201
    except Exception as e:
        db.session.rollback()
        print("Error:", str(e))  # Debugging log
        return jsonify({'message': 'Error registering user', 'error': str(e)}), 500

#create a login route
@auth.route('/login', methods=['POST'])
def login():
    #get the data from the request
    data = request.get_json()
    #find the user by email
    user = NutritionLog.query.filter_by(email=data['email']).first()
    #if the user is not found or the password is incorrect return a message
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password!'}), 401
    #generate a token
    token = jwt.encode({
        'user_id': user.user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }, JWT_SECRET_KEY, algorithm="HS256")
    #return the token and the user
    return jsonify({
        'token': token,
        'user': user.to_dict()
    })

CORS(app)