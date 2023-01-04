from flask import Flask,jsonify,request
from pymongo import MongoClient


app = Flask(__name__)


client = MongoClient("mongo")
mydb=client['Users']
mycol=mydb['user']


@app.route('/')
def home():
    return jsonify("Hello Dockerized CRUD Flask Application Using MongoDB !!")


@app.route('/create',methods=['POST'])
def create():
    id = request.json['id']
    name = request.json['name']
    age = request.json['age']
    mycol.insert_one({'id':id,'name':name,'age':age})
    resp = {'message':'User Added Successfully','success':True}
    return resp


@app.route('/read',methods=['GET'])
def read():
    args = request.args
    id = int(args.get('id'))
    users = mycol.find_one({'id':id})
    if users != None:
        resp = {'ID':users['id'],'Name':users['name'],'Age':users['age']}
        return resp
    else:
        resp = {'message':'User Not Found','success':False}
        return resp


@app.route('/update',methods=['PUT'])
def update():
    args = request.args
    id = int(args.get('id'))
    users = mycol.find_one({'id':id})
    if users != None:
        name = args.get('name')
        age = args.get('age')
        mycol.update_one({'id':id},{'$set':{'name':name,'age':age}})
        resp = {'message':'User Updated Successfully','success':True}
        return resp
    else:
        resp = {'message':'User Not Found','success':False}
        return resp


@app.route('/delete',methods=['DELETE'])
def delete():
    args = request.args
    id = int(args.get('id'))
    users = mycol.find_one({'id':id})
    if users != None:
        mycol.delete_one({'id':id})
        resp = {'message':'User Deleted Successfully','success':True}
        return resp
    else:
        resp = {'message':'User Not Found','success':False}
        return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)