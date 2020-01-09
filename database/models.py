from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
from app import app
from datetime import datetime, timedelta
db = SQLAlchemy()

class User(db.Model):
    id =  db.Column( db.Integer, primary_key=True)
    username =  db.Column( db.String(64), index=True, unique=True)
    email =  db.Column( db.String(120), index=True, unique=True)
    hashed_password =  db.Column( db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)   

    def generate_token(self, user_id):
        """ 
        Generates the access token
        
        Parameters
        ----------
        user_id: int
            Id of user for which we want to generate access token

        Returns
        -------
        str
            If succeded returns access_token of user
            If not - returns exception
        """

        try:
            # Set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=10),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # Create the byte string token using the payload and the SECRET KEY
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # Return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """ 
        Decodes the access token from the Authorization header.
        
        Parameters
        ----------
        token : str
            Access token of a user

        Returns
        -------
        status
            1   If succeded validation
            str If not - returns exception
        """
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

class Hash(db.Model):
    id =  db.Column( db.Integer, primary_key=True)
    hash_type =  db.Column( db.String(10))
    hashed_text =  db.Column( db.String(512), unique=True)
    plain_text =  db.Column( db.String(512), unique=True)

    def __init__(self, hash_type, hashed_text, plain_text):
        self.hash_type = hash_type
        self.hashed_text = hashed_text
        self.plain_text = plain_text