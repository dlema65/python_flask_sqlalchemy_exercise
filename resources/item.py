from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Este campo no puede estar vacío"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Todo artículo requiere un identificador de almacén"
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404


    @jwt_required()
    def post(self, name ):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f'an item with name {name} already exists'}, 400
        payload = Item.parser.parse_args()
        item = ItemModel(name, **payload)

        try:
            item.save_to_db()
        except:
            return {"message": "an error occurred inserting item"}, 500

        return item.json(), 201


    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'item deleted'}, 201

        return{'message': 'item not found'}, 404


    @jwt_required()
    def put(self, name):
        payload = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price(payload['price'])
            item.store_id(payload['store_id'])
        else:
            item = ItemModel(name, **payload)

        item.save_to_db()

        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
