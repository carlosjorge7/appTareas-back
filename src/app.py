from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/flask-react'
app.config['UPLOAD_FOLDER'] = './Uploads'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users


@app.route('/upload', methods=['POST'])
def upload():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['file']
  filename = secure_filename(f.filename)
  # Guardamos el archivo en el directorio "Archivos PDF"
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  # Retornamos una respuesta satisfactoria
  return jsonify({
    'route': 'C:/Users/carlos.jorge/OneDrive - Accenture/Desktop/Python/angular-flask-crud/backend/Uploads/'+filename
  })

@app.route('/users', methods=['POST'])
def create_user():
    #print(request.json)
    id = db.insert({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    return jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in db.find():
        users.append({
            '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'User deleted'})

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({'message': 'User Updated'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)