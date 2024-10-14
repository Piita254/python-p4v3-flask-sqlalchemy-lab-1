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

@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake =  Earthquake.query.filter(Earthquake.id==id).first()

    if earthquake:
        resp_body= {
             "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        return make_response (jsonify(resp_body),200)
    else:
        resp_body = {"message": f"Earthquake {id} not found."}
        return make_response(jsonify(resp_body), 404) 

@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude_value(magnitude):
    earthquakes = []
    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        earthquake_dict = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        earthquakes.append(earthquake_dict)
    body = {'count': len(earthquakes), 'quakes': earthquakes}
    status = 200
    return jsonify(body)



    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
