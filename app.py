from flask import Flask
from hashlib import new
import json
from flask import Flask , render_template , request , redirect , url_for, jsonify
from flask_cors import cross_origin , CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://czqz@localhost:5432/TENNISMATE'
db = SQLAlchemy(app)
CORS(app)

#database setups

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer , primary_key = True)
    user_name = db.Column(db.String() , nullable = False)
    user_email = db.Column(db.String() , nullable = False)
    password = db.Column(db.String() , nullable = False)
    #properties for each user object

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

@app.route('/create_user' , methods=['POST'])
def createUser():
    req = request.get_json()
    new_user = User(user_id = req['user_id'] , user_name = req['user_name'] , user_email = req['user_email'] , password = req['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(req)

@app.route('/get_user_info', methods = ['GET'])
def get_all_user():   
    rows = []
    for users_key in User.query.all():
        each_user = User.query.get(users_key.user_id)
        rows.append({
            "user_id": each_user.user_id,
            "user_name": each_user.user_name,
            "user_email": each_user.user_email,
            "password": each_user.password
        })
    return jsonify(rows)

@app.route('/delete_user/<id>' , methods=['DELETE'])
def delete_user(id):
    print(id)
    try:
        todel = User.query.get(id)
        db.session.delete(todel)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify(id)

#########################################################
#########################################################
#                        API for posts

@app.route('/create_post' , methods=['POST'])
def createPost():
    req = request.get_json()
    print(req)
    new_post = Post(id= req['id'] , courtName = req['courtName'] , email = req['email'] , img_url = req['img_url'] , date =req['date'], location = req['location'], skillLevel = req['skillLevel'], eventSize= req['eventSize'], currentPeople = req['currentPeople'])
    print(new_post)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(req)

@app.route('/get_post', methods = ['GET'])
def get_all_posts():   
    rows = []
    for posts_key in Post.query.all():
        each_post = Post.query.get(posts_key.id)
        rows.append({
            "id": each_post.id,
            "courtName": each_post.courtName,
            "email": each_post.email,
            "date": each_post.date,
            "location": each_post.location,
            "skillLevel": each_post.skillLevel,
            "currentPeople": each_post.currentPeople,
            "img_url": each_post.img_url
        })
    return jsonify(rows)

@app.route('/delete_post/<id>' , methods=['DELETE'])
def delete_post(id):
    print(id)
    try:
        todel = Post.query.get(id)
        db.session.delete(todel)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify(id)

@app.route('/add_person/<id>' , methods=['POST'])
def add_person(id):
    print(id)
    try:
        toadd = Post.query.get(id)
        toadd.currentPeople = toadd.currentPeople + 1 
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify(id)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"