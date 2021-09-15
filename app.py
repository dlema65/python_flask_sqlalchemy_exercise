import os

from db import db
from flask_restful import Resource, Api, reqparse
from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['JWT_SECRET_KEY'] = 'no-escribirla-aquí' # esto es solo un ejemplo
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

jwt = JWTManager(app)

#Crea una ruta para autenticación
@app.route("/login", methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username and password and authenticate(username, password):
        access_token = create_access_token(identity=username)
        return access_token
    return {'message': 'bad username or password'}, 401

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
