from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


    # function to turn SQLAlchemy Object Queried to a Dictionary
    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record

@app.route("/random")
def random_cafe():
    all_cafes = Cafe.query.all()  # --> get all cafe data in db
    print(all_cafes)
    random_cafe = random.choice(all_cafes)  # --> pick a random cafe

    # now, jsonify your SQLAlchemy object
    json_random_cafe = jsonify(
        name=random_cafe.name,
        map_url=random_cafe.map_url,
        img_url=random_cafe.img_url,
        location=random_cafe.location,
        has_sockets=random_cafe.has_sockets,
        has_toilet=random_cafe.has_toilet,
        has_wifi=random_cafe.has_wifi,
        can_take_calls=random_cafe.can_take_calls,
        seats=random_cafe.seats,
        coffee_pirce=random_cafe.coffee_price
    )

    return json_random_cafe # return that json so flask serve it up

@app.route("/all")
def all():

    cafes_list = []
    all_cafes = Cafe.query.all()

    for cafe in all_cafes:

        each_cafe = {
        "name":cafe.name,
        "map_url":cafe.map_url,
        "img_url":cafe.img_url,
        "location":cafe.location,
        "has_sockets":cafe.has_sockets,
        "has_toilet":cafe.has_toilet,
        "has_wifi":cafe.has_wifi,
        "can_take_calls":cafe.can_take_calls,
        "seats":cafe.seats,
        "coffee_price":cafe.coffee_price
        }

        cafes_list.append(each_cafe)
    
    return jsonify(cafes=cafes_list)
    
@app.route("/search", methods=["GET"])
def search():

    message = {
        "error":{
            "Not Found" : "Cafe at that location is not available."
        }
    }

    cafe_list =[]
    query_location = request.args.get("loc")
    cafes = db.session.query(Cafe).filter_by(location=query_location).all()
    if cafes:
        for cafe in cafes:
            each_cafe = cafe.to_dict()
            cafe_list.append(each_cafe)
        
        return jsonify(cafes=cafe_list)
        
    else:
        return jsonify(
            message
        )



## HTTP POST - Create Record

@app.route("/add", methods=["POST","GET"])
def add():
    new_data = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(int(request.form.get("has_sockets"))),
        has_toilet=bool(int(request.form.get("has_toilet"))),
        has_wifi=bool(int(request.form.get("has_wifi"))),
        can_take_calls=bool(int(request.form.get("can_take_calls"))),
        seats=request.form.get("seats"),
        coffee_price = request.form.get("coffee_price")
    )

    db.session.add(new_data)
    db.session.commit()
    return jsonify(result={
        "Success" : "Added Succesfully"
    })



## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<int:id>", methods=["PATCH"])
def update_price(id):
    cafe_id = id
    new_price = request.args.get("new_price")
    cafe_where_price_needs_to_be_replaced = db.session.query(Cafe).get(cafe_id)
    if cafe_where_price_needs_to_be_replaced:
        cafe_where_price_needs_to_be_replaced.coffee_price = new_price
        db.session.commit()
        return jsonify({
            "Success" : "Price is Updated"
        })
    else:
        return jsonify({
            "Failure" : "Cafe does not exist"
        })
    

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
