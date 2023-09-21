#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery is None:
        return jsonify({'message': 'Bakery not found'}), 404

    data = request.form

    if 'name' in data:
        bakery.name = data['name']

    db.session.commit()

    return jsonify(bakery.to_dict()), 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()

    response = make_response(
        bakery_serialized,
        200
    )
    return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form

    if 'name' not in data or 'price' not in data or 'bakery_id' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    baked_good = BakedGood(
        name=data['name'],
        price=data['price'],
        bakery_id=data['bakery_id']
    )
    db.session.add(baked_good)
    db.session.commit()

    return jsonify(baked_good.to_dict()), 201

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()

    if baked_good is None:
        return jsonify({'message': 'Baked Good not found'}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({'message': 'Baked Good deleted successfully'}), 200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
