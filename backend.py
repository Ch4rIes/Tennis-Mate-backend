from flask import Flask
from hashlib import new
import json
from flask import Flask , render_template , request , redirect , url_for, jsonify
from flask_cors import cross_origin , CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, logout_user
from flask_login import UserMixin, login_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://czqz@localhost:5432/TENNISMATE'
db = SQLAlchemy(app)
CORS(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
app.secret_key = "wellthisisasecretkey"

class User(db.Model , UserMixin):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer , primary_key = True)
    user_name = db.Column(db.String() , nullable = False)
    user_email = db.Column(db.String() , nullable = False)
    password = db.Column(db.String() , nullable = False)
    #properties for each user object
    def get_id(self):
           return (self.user_id)

class Post(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer , primary_key = True)
    courtName = db.Column(db.String() , nullable = False)
    date = db.Column(db.String() , nullable = False)
    location = db.Column(db.String() , nullable = False)
    skillLevel = db.Column(db.String() , nullable = False)
    email = db.Column(db.String() , nullable = False)
    eventSize = db.Column(db.Integer() , nullable = False)
    currentPeople = db.Column(db.Integer() , nullable = False)
    img_url = db.Column(db.String() , nullable = False) #we render a picture using the url provided

db.create_all()
import postAPI
import userAPI
#database setups

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#########################################################
#########################################################
#                        API for posts
@app.route("/login" , methods=['GET','POST'])
def login():
    req = request.get_json()
    inputUserEmail = req['user_email']
    target_user = User.query.filter_by(user_email = inputUserEmail).first()
    loginStatus = False
    if target_user and bcrypt.check_password_hash(target_user.password , req['password'].encode('utf-8')):
        #user exist and the password is right 
        login_user(target_user)
        loginStatus = True
    return jsonify({'ifLogedIn': loginStatus})
@app.route("/logout")
def logout():
    logout_user()
    return jsonify('')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"