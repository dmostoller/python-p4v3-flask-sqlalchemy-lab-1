# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    if not earthquake:
        earthquake_res = {
            "message" : f"Earthquake {id} not found."
        }
        response = make_response(jsonify(earthquake_res), 404)
    else:
        earthquake_res = {
            "id" : earthquake.id, 
            "location" : earthquake.location,
            "magnitude" : earthquake.magnitude,
            "year" : earthquake.year
        }
        response = make_response(jsonify(earthquake_res), 200)
    return response

@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    earthquake_count = len(earthquakes)
    quakes = []
    for earthquake in earthquakes:
        quake_res = {
            "id" : earthquake.id, 
            "location" : earthquake.location,
            "magnitude" : earthquake.magnitude,
            "year" : earthquake.year
        }
        quakes.append(quake_res)

    earthquake_res = {
        "count": earthquake_count,
        "quakes" : quakes
    }
    response = make_response(jsonify(earthquake_res), 200)
    return response
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
