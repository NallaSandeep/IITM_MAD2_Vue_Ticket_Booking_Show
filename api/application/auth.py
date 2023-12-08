from application.models import User
from flask import current_app as app
from flask import request, make_response, jsonify
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from .validation import AuthenticationError, BadRequestError, NotFoundError
from .validation import handle_authentication_error, handle_bad_request_error, handle_not_found_error
from .database import db


# Ref: https://www.geeksforgeeks.org/using-jwt-for-user-authentication-in-flask/
# decorator for verifying the JWT
def token_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request header
            if 'Authentication-Token' in request.headers:
                token = request.headers['Authentication-Token']
            # return 401 if token is not passed
            if not token:
                raise AuthenticationError('Token is missing')
            try:
                # decoding the payload to fetch the stored details
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                # print(data)
                current_user = User.query\
                    .filter_by(id = data['id'])\
                    .first()
            except jwt.ExpiredSignatureError:
                raise AuthenticationError('Token has expired')
            except jwt.InvalidTokenError:
                raise AuthenticationError('Invalid token')
            except Exception as e:
                raise AuthenticationError(str(e))
            # Extract the username from the path parameter
            user_id_from_path = kwargs.get('user_id')
            onlyAdminAccess = len(roles) == 1 and "admin" in roles
            # Compare the username from the path with the one from the JWT payload
            if user_id_from_path != None and user_id_from_path != data['id']:
                raise AuthenticationError('Unauthorized access')
            if(onlyAdminAccess and not int(current_user.is_admin) == 1):
                raise AuthenticationError('Only Admin can access')
            # returns the current logged in users context to the routes
            return  f(current_user, *args, **kwargs)  
        return decorated
    return decorator

# route for logging user in
@app.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    auth = request.form
    
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 400 if any email or / and password is missing
        raise BadRequestError("Email or Password is missing")
  
    user = User.query\
        .filter_by(email = auth.get('email'))\
        .first()
  
    if not user:
        # returns 404 if user does not exist
        raise NotFoundError("User not found. Please Create an account")
  
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'id': user.id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
  
        return make_response(jsonify({'id': user.id, 'username': user.username, 'email': user.email,'token' : token, 'isAdmin': user.is_admin}), 200)
    # returns 400 if password is wrong
    raise BadRequestError("Email or Password is invalid")
  
# signup route
@app.route('/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form
  
    # gets username, email and password
    username, email = data.get('username'), data.get('email')
    password = data.get('password')
    isAdmin = data.get('isAdmin')
  
    # checking for existing user
    user = User.query\
        .filter_by(email = email)\
        .first()
    if not user:
        # database ORM object
        user = User(
            fs_uniquifier = str(uuid.uuid4()),
            username = username,
            email = email,
            password = generate_password_hash(password),
            is_admin = isAdmin
        )
        # insert user
        db.session.add(user)
        db.session.commit()
  
        if check_password_hash(user.password, data.get('password')):
        # generates the JWT Token
            token = jwt.encode({
                'id': user.id,
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return make_response(jsonify({'id': user.id, 'username': user.username, 'email': user.email,'token' : token, 'isAdmin': user.is_admin}), 201)
    else:
        # returns 400 if user already exists
        raise BadRequestError("User already exists")