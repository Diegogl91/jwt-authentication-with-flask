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
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from models import db, User, Planet, People, Favorites
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'a7656fafe94dae72b1e1487670148412'
MIGRATE = Migrate(app, db)
jwt = JWTManager(app)
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

@app.route('/api/people', methods=['GET','POST'])
def get_peoples():

    if request.method == 'GET':
        peoples = People.query.all()
        peoples = list(map(lambda peoples: peoples.serialize(), peoples))

        return jsonify(peoples), 200
    
    if request.method == 'POST':
        name = request.json.get('name')
        height = request.json.get('height')
        mass = request.json.get('mass')
        hair_color = request.json.get('hair_color')
        skin_color = request.json.get('skin_color')
        eye_color = request.json.get('eye_color')
        birth_year = request.json.get('birth_year')
        gender = request.json.get('gender')

        people = People()
        people.name = name
        people.height = height
        people.mass = mass
        people.hair_color = hair_color
        people.skin_color = skin_color
        people.eye_color = eye_color
        people.birth_year = birth_year
        people.gender = gender
        people.save()

        return jsonify(people.serialize()),201


@app.route("/api/people/<int:id>", methods=['GET'])
def get_people(id):
    people = People.query.get(id)
    if not people: return jsonify({"status": False, "msg": "People not found!"}), 404
    else:
        return jsonify(people.serialize()), 200

@app.route('/api/planet', methods=['GET','POST'])
def get_planets():
    
    if request.method == 'GET':
        planets = Planet.query.all()
        planets = list(map(lambda planets: planets.serialize(), planets))

        return jsonify(planets), 200
    
    if request.method == 'POST':
        name = request.json.get('name')
        diameter = request.json.get('diameter',"")
        population = request.json.get('population',"")
        climate = request.json.get('climate',"")
        terrain = request.json.get('terrain',"")
        surface_water = request.json.get('surface_water',"")
        gravity = request.json.get('gravity',"")
        rotation_period = request.json.get('rotation_period',"")

        planet = Planet()
        planet.name = name
        planet.diameter = diameter
        planet.population = population
        planet.climate = climate
        planet.terrain = terrain
        planet.surface_water = surface_water
        planet.gravity = gravity
        planet.rotation_period = rotation_period
        planet.save()
        return jsonify(planet.serialize()),201

@app.route("/api/planet/<int:id>", methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    if not planet: return jsonify({"status": False, "msg": "Planet not found!"}), 404
    else:
        return jsonify(planet.serialize()), 200


@app.route('/api/users', methods=['GET','POST'])
def get_users():

    if request.method == 'GET':
        users = User.query.all()
        users = list(map(lambda user: user.serialize(), users))

        return jsonify(users), 200

    if request.method == 'POST':
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')

        user = User()
        user.name = name
        user.email = email
        user.password = password
        user.safe()

        return jsonify(user.serialize())


@app.route('/api/users/<int:id>/favorites', methods=['GET'])
def get_favorites_by_user(id):
    user = User.query.get(id)
    
    return jsonify(user.serialize_with_favorite()), 200
 
@app.route('/api/favorites/planet/<int:planet_id>', methods=['POST','DELETE'])
def set_favorite_planet(planet_id):
    if request.method == 'POST':

        user = User.query.get(1)
        planet = Planet.query.get(planet_id)
        if not user: return jsonify({ "message": 'There is no user with this id', "status_code": 400 }),400
        if not planet: return jsonify({ "message": 'There is no planet with this id', "status_code": 400 }),400

        user.favorites_planet.append(planet)
        user.save()
        return jsonify({"message": "Success!", "data": user.serialize_with_favorite()})
    
    if request.method == 'DELETE':
        user = User.query.get(1)
        planet = Planet.query.get(planet_id)
        print(planet)
        if not user: return jsonify({ "message": 'There is no user with this id', "status_code": 400 }),400
        if not planet: return jsonify({ "message": 'There is no planet with this id', "status_code": 400 }),400

        user.favorites_planet.remove(planet)
        user.save()
        return jsonify({"message": "Success!", "data": user.serialize_with_favorite()})


@app.route('/api/favorites/people/<int:people_id>', methods=['POST','DELETE'])
def set_favorite_people(people_id):
    if request.method == 'POST':

        user = User.query.get(1)
        people = People.query.get(people_id)
        if not user: return jsonify({ "message": 'There is no user with this id', "status_code": 400 }),400
        if not people: return jsonify({ "message": 'There is no people with this id', "status_code": 400 }),400

        user.favorites_people.append(people)
        user.save()
        return jsonify({"message": "Success!", "data": user.serialize_with_favorite()})
    
    if request.method == 'DELETE':
        user = User.query.get(1)
        people = People.query.get(people_id)
        if not user: return jsonify({ "message": 'There is no user with this id', "status_code": 400 }),400
        if not people: return jsonify({ "message": 'There is no people with this id', "status_code": 400 }),400

        user.favorites_people.remove(people)
        user.save()
        return jsonify({"message": "Success!", "data": user.serialize_with_favorite()})

@app.route('/api/signup', methods=['POST'])
def signup():

    name = request.json.get('name', "")
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if user: return jsonify({ "msg": "Email ya esta en uso."}), 400

    user = User()
    user.name = name
    user.email = email
    user.password = generate_password_hash(password)
    user.save()

    return jsonify({ "msg": "Usuario registrado. por favor inicie session"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if not user: 
        return jsonify({"msg": "Usuario/contraseña no se encuentran"}), 400

    if not check_password_hash(user.password,password): 
        return jsonify({"msg": "Usuario/contraseña no se encuentran"}), 400

    access_token = create_access_token(identity=user.email)

    data = {
        "access_token": access_token,
        "user": user.serialize()
    }


    return jsonify(data),200









# def post_favoritePlanets_by_user(planet_id):

#     json = request.get_json()
#     user = str(json['user'])

#     if request.method == 'POST':
#         favorite = Favorites()
#         favorite.tipo = "planet"
#         favorite.favorite_id = planet_id
#         favorite.user_id = user
#         favorite.name = str(json['name'])
#         favorite.save()
 
#         return jsonify("Successfully added"), 201
        

#     if request.method == 'DELETE':
#         favorite = Favorites.query.filter_by(favorite_id=planet_id, tipo="planet", user_id = user).first()
#         favorite.delete()

#         return jsonify({ "success": "Planet deleted from favorites"}), 200


@app.route('/api/favorites/people/<int:people_id>', methods=['POST','DELETE'])
def post_favoritePeople_by_user(people_id):

    json = request.get_json()
    user = str(json['user'])

    if request.method == 'POST':
        favorite = Favorites()
        favorite.tipo = "people"
        favorite.favorite_id = people_id
        favorite.user_id = user
        favorite.name = str(json['name'])
        favorite.save()
 
        return jsonify("Successfully added"), 201
        

    if request.method == 'DELETE':
        favorite = Favorites.query.filter_by(favorite_id=people_id, tipo="people", user_id = user).first()
        favorite.delete()

        return jsonify({ "success": "Planet deleted from favorites"}), 200


    

           


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

