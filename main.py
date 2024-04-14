from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean
import random

# Initialize SQLAlchemy with no model class
db = SQLAlchemy()

# Define model outside of create_app
class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), unique=True, nullable=False)
    map_url = db.Column(String(500), nullable=False)
    img_url = db.Column(String(500), nullable=False)
    location = db.Column(String(250), nullable=False)
    seats = db.Column(String(250), nullable=False)
    has_toilet = db.Column(Boolean, nullable=False)
    has_wifi = db.Column(Boolean, nullable=False)
    has_sockets = db.Column(Boolean, nullable=False)
    can_take_calls = db.Column(Boolean, nullable=False)
    coffee_price = db.Column(String(250), nullable=True)

def create_app(db_uri='sqlite:///cafes.db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/random")
    def get_random():
        rows = db.session.query(Cafe).all()
        random_cafe = random.choice(rows)
        return jsonify(cafe={
            'name': random_cafe.name,
            'map_url': random_cafe.map_url,
            'img_url': random_cafe.img_url,
            'location': random_cafe.location,
            'seats': random_cafe.seats,
            'has_toilet': random_cafe.has_toilet,
            'has_wifi': random_cafe.has_wifi,
            'has_sockets': random_cafe.has_sockets,
            'can_take_calls': random_cafe.can_take_calls,
            'coffee_price': random_cafe.coffee_price
        })

    @app.route("/all")
    def get_all():
        rows = db.session.query(Cafe).all()
        all_cafes = [{'name': cafe.name, 'map_url': cafe.map_url, 'img_url': cafe.img_url,
                      'location': cafe.location, 'seats': cafe.seats, 'has_toilet': cafe.has_toilet,
                      'has_wifi': cafe.has_wifi, 'has_sockets': cafe.has_sockets, 'can_take_calls': cafe.can_take_calls,
                      'coffee_price': cafe.coffee_price} for cafe in rows]
        return jsonify(cafes=all_cafes)

    @app.route("/add", methods=["POST"])
    def post_new_cafe():
        new_cafe = Cafe(
            name=request.form["name"],
            map_url=request.form["map_url"],
            img_url=request.form["img_url"],
            location=request.form["loc"],
            has_sockets=request.form.get("sockets", type=bool),
            has_toilet=request.form.get("toilet", type=bool),
            has_wifi=request.form.get("wifi", type=bool),
            can_take_calls=request.form.get("calls", type=bool),
            seats=request.form["seats"],
            coffee_price=request.form["coffee_price"],
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})

    @app.route('/update-cafe/<int:id>', methods=['PATCH'])
    def update_cafe(id):
        cafe = db.session.get(Cafe, id)
        if cafe:
            cafe.coffee_price = request.args.get('new_price', cafe.coffee_price)
            db.session.commit()
            return jsonify(success='Successfully updated the price.')
        else:
            return jsonify(error='Not found')

    @app.route('/report-close/<int:id>', methods=['DELETE'])
    def delete_cafe(id):
        cafe = db.session.get(Cafe, id)
        api_key = request.args.get('api_key', '')
        if cafe and api_key == 'secret':
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(success='Successfully reported cafe as closed.')
        else:
            return jsonify(error='Unauthorized or cafe does not exist')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
