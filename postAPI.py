from backend import app, db, Post
import json
from flask import Flask , render_template , request , redirect , url_for, jsonify
from flask_cors import cross_origin , CORS
from flask_sqlalchemy import SQLAlchemy


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


@app.route('/create_post' , methods=['POST'])
def createPost():
    req = request.get_json()
    print(req)
    new_post = Post(id= req['id'] , courtName = req['courtName'] , email = req['email'] , img_url = req['img_url'] , date =req['date'], location = req['location'], skillLevel = req['skillLevel'], eventSize= req['eventSize'], currentPeople = req['currentPeople'])
    print(new_post)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(req)



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

@app.route('/add_person/<id>' , methods= ['GET' , 'POST'])
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