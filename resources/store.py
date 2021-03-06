from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.store import StoreModel

class Store(Resource):


    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'store not found'}, 404


    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "store '{}' already exists".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return{"message": "Ocurrió un error durante la creación de la tienda"}, 500

        return store.json(), 201


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "store '{}' deleted".format(name)}
        return {"message": "store '{}' did not exist".format(name)}, 404


class StoreList(Resource):

    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
