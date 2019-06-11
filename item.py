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
        item = Item.find_by_name(name)
        if item is not None:
            return item
        return {'msg': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row is not None:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        #     return {'msg': 'An item with name "{}" already exists'.format(name)}

        if Item.find_by_name(name) is not None:
            return {'msg': 'An item with name "{}" already exists'.format(name)}

        # request_data = request.get_json()
        request_data = Item.parser.parse_args()
        newitem = {
            'name': name,
            'price': request_data['price']
        }

        # items.append(newitem)
        try:
            Item.insert(newitem)
        except:
            return {'msg': 'An error occured while inserting item'}, 500    # internal server error
        
        return newitem, 201

    @classmethod
    def insert(cls, newitem):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?, ?)"

        cursor.execute(query, (newitem['name'], newitem['price']))
        connection.commit()
        connection.close()


    def delete(self, name):
        # global items
        # items = list(filter(lambda x : x['name'] != name, items))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return { 'msg': 'item has been deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = Item.find_by_name(name)
        updated_Item = {
                'name' : name,
                'price': data['price']
            }

        if item is None:
            try:
                Item.insert(updated_Item)
            except:
                return {'msg' : 'An error occured while inserting'}, 500
            # items.append(newItem)
        else:
            try:
                Item.update(updated_Item)
            except:
                return {'msg' : 'An error occured while updating'}, 500
            return updated_Item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        return {'items': items}
