import os
from dataclasses import dataclass

from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from producer import Producer

app = Flask(__name__)
CORS(app)
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    likes: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.TEXT(20000000))
    likes = db.Column(db.Integer, default=0)


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    # define a static user id for demo
    producer = Producer()
    try:
        product = Product.query.get(id)
        product.likes += 1
        db.session.commit()

        producer.publish('product_liked', id)
    except:
        abort(400, 'bad request')

    return jsonify(product)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
