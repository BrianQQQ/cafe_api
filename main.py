from flask import Flask, jsonify, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(Cafe).where(Cafe.name == "Louisa")):
        cafe = Cafe(name='Louisa',
                    map_url='http://google.com',
                    img_url='http://example.com/img.jpg',
                    location='Taiwan',
                    seats='100',
                    has_toilet=True,
                    has_wifi=True,
                    has_sockets=True,
                    can_take_calls=True,
                    coffee_price='100')

        db.session.add(cafe)
        db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random():
    rows = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(rows)
    return jsonify( cafe={
                    'name':random_cafe.name,
                    'map_url':random_cafe.map_url,
                    'img_url':random_cafe.img_url,
                    'location':random_cafe.location,
                    'seats':random_cafe.seats,
                    'has_toilet':random_cafe.has_toilet,
                    'has_wifi':random_cafe.has_wifi,
                    'has_sockets':random_cafe.has_sockets,
                    'can_take_calls':random_cafe.can_take_calls,
                    'coffee_price':random_cafe.coffee_price})

@app.route("/all")
def get_all():
    rows = db.session.execute(db.select(Cafe)).scalars().all()
    all_cafes = []
    for cafe in rows:
        cafe_json = {'name':cafe.name,
                    'map_url':cafe.map_url,
                    'img_url':cafe.img_url,
                    'location':cafe.location,
                    'seats':cafe.seats,
                    'has_toilet':cafe.has_toilet,
                    'has_wifi':cafe.has_wifi,
                    'has_sockets':cafe.has_sockets,
                    'can_take_calls':cafe.can_take_calls,
                    'coffee_price':cafe.coffee_price}
        all_cafes.append(cafe_json)
    return jsonify(cafes=all_cafes)

@app.route('/search')
def search_cafe():
    loc = request.args.get('loc', '')
    result = db.session.execute(db.select(Cafe).where(Cafe.location == loc)).scalar()
    if not result:
        return jsonify(error={'Not Found':'Sorry, we don\'t have a cafe at that location.'})
    else:
        result_json = {
                        'name':result.name,
                        'map_url':result.map_url,
                        'img_url':result.img_url,
                        'location':result.location,
                        'seats':result.seats,
                        'has_toilet':result.has_toilet,
                        'has_wifi':result.has_wifi,
                        'has_sockets':result.has_sockets,
                        'can_take_calls':result.can_take_calls,
                        'coffee_price':result.coffee_price 
                        }
        return jsonify(cafe=result_json)


# HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record

@app.route('/update-cafe/<int:id>', methods=['PATCH'])
def update_cafe(id):
    cafe_id = db.get_or_404(Cafe, id)
    if cafe_id:
        cafe_id.coffee_price = request.args.get('new_price', '')
        db.session.commit()
        return {'success': 'Successfully update the price.'}
    else:
        return {'Not found': 'Sorry'}

# HTTP DELETE - Delete Record

@app.route('/report-close/<int:id>', methods=['DELETE'])
def delete_cafe(id):
    cafe_id = db.get_or_404(Cafe, id)
    api_key = request.args.get('api_key', '')
    if cafe_id and api_key == 'secret':
        db.session.delete(cafe_id)
        db.session.commit()
        return {'success': 'Successfully report close.'}
    else:
        return {'Unauthorized': 'Sorry'}

if __name__ == '__main__':
    app.run(debug=True)
