from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, CarInventory, carInventory_schema, carInventories_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}
#id, name, email, brand, make, user-token
@api.route('/carinventory', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    email = request.json['email']
    brand = request.json['brand']
    make = request.json['make']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = CarInventory(name, email, brand, make, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = carInventory_schema.dump(car)
    return jsonify(response)

@api.route('/carinventory', methods = ['GET'])
@token_required

def get_car(current_user_token):
    a_user = current_user_token.token
    cars = CarInventory.query.filter_by(user_token = a_user).all()
    response = carInventories_schema.dump(cars)
    return jsonify(response)

@api.route('/carinventory/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = CarInventory.query.get(id)
    response = carInventory_schema.dump(car)
    return jsonify(response)

@api.route('/carinventory/<id>', methods = ['POST', 'PUT'])
@token_required
def update_inventory(current_user_token, id):
    car = CarInventory.query.get(id)
    car.name = request.json['name']
    car.email = request.json['email']
    car.brand = request.json['brand']
    car.make = request.json['make']

    db.session.commit()
    response = carInventory_schema.dump(car)
    return jsonify(response)

@api.route('/carinventory/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = CarInventory.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = carInventory_schema.dump(car)
    return jsonify(response)
