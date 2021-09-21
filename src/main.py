"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

@app.route('/api/people', methods=['GET'])
def get_peoples():
    peoples = People.query.all()
    peoples = list(map(lambda peoples: peoples.serialize(), peoples))

    return jsonify(peoples), 200

@app.route("/api/people/<int:id>", methods=['GET'])
def get_people(id):
    people = People.query.get(id)
    if not people: return jsonify({"status": False, "msg": "People not found!"}), 404
    else:
        return jsonify(people.serialize()), 200

@app.route('/api/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planets: planets.serialize(), planets))

    return jsonify(planets), 200

@app.route("/api/planet/<int:id>", methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    if not planet: return jsonify({"status": False, "msg": "Planet not found!"}), 404
    else:
        return jsonify(planet.serialize()), 200


@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/api/users/<int:id>/favorites', methods=['GET'])
def get_favorites_by_user(id):
    favorites = Favorites.query.get(id)
    
    return jsonify(favorites.serialize()), 200

# @app.route('/api/users', methods=['POST'])
# def post_users():

#     name = request.json.get('name')
#     email = request.json.get('email')
#     password = request.json.get('password')

#     user = User()
#     user.name = name
#     user.email = email
#     user.password = password
#     user.save()

#     return jsonify(user.serialize()), 201


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

