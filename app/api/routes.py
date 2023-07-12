from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whiskey, whiskey_schema, whiskey_schemas

api = Blueprint('api', __name__, url_prefix='/api')

# @api.route('getdata')
# def getdata():
#     return {'yee': 'haw'}

@api.route('/whiskey', methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    name = request.json['name']
    type = request.json['type']
    price = request.json['price']
    year_made = request.json['year_made']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    whiskey = Whiskey(name, type, price, year_made, user_token=user_token)

    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey', methods = ['GET'])
@token_required
def get_whiskey(current_user_token):
    a_user = current_user_token.token
    whiskey = Whiskey.query.filter_by(user_token = a_user).all()
    response = whiskey_schemas.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    whiskey.name = request.json['name']
    whiskey.type = request.json['type']
    whiskey.price = request.json['price']
    whiskey.year_made = request.json['year_made']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)