from backend import app, db, User, bcrypt
import json
from flask import Flask , render_template , request , redirect , url_for, jsonify
from flask_cors import cross_origin , CORS
from flask_sqlalchemy import SQLAlchemy




@app.route('/create_user' , methods=['POST'])
def createUser():
    req = request.get_json()
    hashedpassowrd = bcrypt.generate_password_hash(req['password'].encode('utf-8')).decode('utf-8')
    new_user = User(user_id = req['user_id'] , user_name = req['user_name'] , user_email = req['user_email'] , password = hashedpassowrd)
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