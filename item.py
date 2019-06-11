import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type = float, required = True, help = "This filed cannot be blank")


    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return item, 200 if item is not None else 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row is not None:
            return {'item': {'name': row[0], 'price': row[1]}}
        return {'msg': 'Item not found'}

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'msg': 'An item with name "{}" already exists'.format(name)}

        # request_data = request.get_json()
        request_data = Item.parser.parse_args()
        newitem = {
            'name': name,
            'price': request_data['price']
        }

        items.append(newitem)
        return newitem, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x : x['name'] != name, items))
        return { 'msg': 'item has been deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            newItem = {
                'name' : name,
                'price': data['price']
            }
            items.append(newItem)
        else:
            item.update(data)
            return item



class ItemList(Resource):
    def get(self):
        return {'items': items}
