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
from models import db, Usuario, Personaje, Planeta
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(Usuario).all()
    print('Usuarios',users)
    list_user = list()
    for user in users:
        print(user)
        print(user.nombre)
        print(user.email)
        list_user.append({"id": user.id,"nombre": user.nombre,"apellido": user.apellido,"email": user.email,"password": user.password})
    print(users)
    return jsonify({"usuarios": list_user}), 200

    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

@app.route('/user', methods=['POST'])
def create_users():
    try:
        user = Usuario()
        user.nombre = request.json.get("nombre")
        user.apellido = request.json.get("apellido")
        user.email = request.json.get("email")
        user.password = request.json.get("password")
        print(user)
        db.session().add(user)
        db.session().commit()
        return jsonify({"message":"create"}), 201
    except Exception as e:
        return jsonify({"message":e}), 500

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planeta = db.session.query(Planeta).get(planet_id)
    print('Planeta',planeta)
    if planeta is not None:
        return jsonify(planeta.serialize()), 200
    else:
        return jsonify({"message":"Planeta not found"}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planetas = db.session.query(Planeta).all()
    print('Planetas',planetas)
    list_planeta = list()
    for planeta in planetas:
        print(planeta)
        print(planeta.nombre)
        print(planeta.clima)
        list_planeta.append(
            {
                "id": planeta.id,
                "nombre": planeta.nombre,
                "rutaimagen": planeta.rutaimagen,
                "habitantes": planeta.habitantes,
                "terreno": planeta.terreno,
                "clima": planeta.clima,
                "periodoOrbita": planeta.periodoOrbita,
                "periodoRotacion": planeta.periodoRotacion,
                "diametro": planeta.diametro
            }
        )
    print(planetas)
    return jsonify({"planetas": list_planeta}), 200


@app.route('/planet', methods=['POST'])
def create_planet():
    try:
        planeta = Planeta()
        planeta.id = request.json.get("id")
        planeta.nombre = request.json.get("nombre")
        planeta.rutaimagen = request.json.get("rutaimagen")
        planeta.habitantes = request.json.get("habitantes")
        planeta.terreno = request.json.get("terreno")
        planeta.clima = request.json.get("clima")
        planeta.periodoOrbita = request.json.get("periodoOrbita")
        planeta.periodoRotacion = request.json.get("periodoRotacion")
        planeta.diametro = request.json.get("diametro")
        print(planeta)
        db.session().add(planeta)
        db.session().commit()
        return jsonify({"message":"create Planet"}), 201
    except Exception as e:
        return jsonify({"message":e}), 500

@app.route('/planets/<int:planet_id>', methods = ['PUT'])
def update_planets(planet_id):
    planeta = db.session.query(Planeta).get(planet_id)
    if planeta is not None:
        planeta.nombre = request.json.get("nombre")
        planeta.rutaimagen = request.json.get("rutaimagen")
        planeta.habitantes = request.json.get("habitantes")
        planeta.terreno = request.json.get("terreno")
        planeta.clima = request.json.get("clima")
        planeta.periodoOrbita = request.json.get("periodoOrbita")
        planeta.periodoRotacion = request.json.get("periodoRotacion")
        planeta.diametro = request.json.get("diametro")
        db.session.commit()
        return jsonify(planeta.serialize()), 200
    else:
        return jsonify({"message":"Planeta not found"}), 404

@app.route('/planet/<int:planet_id>', methods = ['DELETE'])
def delete_planet(planet_id):
    planeta = db.session.query(Planeta).get(planet_id)
    print('Planeta:', planeta)
    if planeta is not None:
        users = planeta.followerPlaneta
        print('Usuarios:', users)
        for user in users:
            user.followingPlaneta.remove(planeta)
        db.session.delete(planeta)
        db.session.commit()
        return jsonify({"msg":"delete planet success"}), 200
    else:
        return jsonify({"message":"Planet not found"}), 404

@app.route('/user/<int:id>/favorite/planet/<int:planet_id>', methods=['POST'])
def create_planetfav(id, planet_id):
    try:
        print(id)
        print(planet_id)
        user = db.session.query(Usuario).get(id)
        # for usuario in user:
        #     print(usuario)
        planeta = db.session.query(Planeta).get(planet_id)
        # for planet in planeta:
        #     print(planet)
        user.followingPlaneta.append(planeta)
        db.session().commit()
        return jsonify({"Usuario":user.nombre, "Planeta": planeta.nombre}), 201
        # return jsonify(user.serialize()), 201
    except Exception as e:
        return jsonify({"message":e}), 500

@app.route('/user/<int:id>/favorite/people/<int:people_id>', methods=['POST'])
def create_planetfavpeople(id, people_id):
    try:
        print(id)
        print(people_id)
        user = db.session.query(Usuario).get(id)
        # for usuario in user:
        #     print(usuario)
        personaje = db.session.query(Personaje).get(people_id)
        # for planet in planeta:
        #     print(planet)
        user.followingPersonaje.append(personaje)
        db.session().commit()
        return jsonify({"Usuario":user.nombre, "Personaje": personaje.nombre}), 201
        # return jsonify(user.serialize()), 201
    except Exception as e:
        return jsonify({"message":e}), 500

@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_favorite(id):
    user = db.session.query(Usuario).get(id)
    planetas = user.followingPlaneta
    print("Planetas: ", planetas)
    list_planetas = list()
    if planetas  is not None:
        for planeta in planetas:
            print(planeta)
            print(planeta.nombre)
            print(planeta.id)
            list_planetas.append(
                {
                    "id": planeta.id, 
                    "nombre": planeta.nombre, 
                    "rutaimagen": planeta.rutaimagen,
                    "habitantes": planeta.habitantes, 
                    "terreno": planeta.terreno,
                    "clima": planeta.clima, 
                    "periodoOrbita": planeta.periodoOrbita, 
                    "periodoRotacion": planeta.periodoRotacion, 
                    "diametro": planeta.diametro
                }
            )
    else:
        list_planetas.append(
            {
                "id": 0, 
                "nombre": "sin registro"
            }
        )
    personajes = user.followingPersonaje
    print("Personaje: ", personajes)
    list_personajes = list()
    if personajes  is not None:
        for personaje in personajes:
            print(personaje)
            print(personaje.nombre)
            print(personaje.id)
            list_personajes.append(
                {
                    "id": personaje.id, 
                    "nombre": personaje.nombre, 
                    "rutaimagen": personaje.rutaimagen,
                    "genero": personaje.genero, 
                    "colorpelo": personaje.colorpelo,
                    "colorojos": personaje.colorojos, 
                    "nacimiento": personaje.nacimiento, 
                    "altura": personaje.altura,
                    "colorpiel": personaje.colorpiel
                }
            )
    else:
        list_personajes.append(
            {
                "id": 0, 
                "nombre": "sin registro"
            }
        )

    return jsonify({"planetas:": list_planetas, "personajes:": list_personajes}), 200
    # return jsonify({"Usuario":user.nombre, "Planeta": planeta.nombre}), 201

@app.route('/user/<int:id>/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_favplanet(id, planet_id):
    user = db.session.query(Usuario).get(id)
    planeta = db.session.query(Planeta).get(planet_id)
    if user is not None and planeta is not None:
        user.followingPlaneta.remove(planeta)
        db.session.commit()
        return jsonify({"msg":"delete success"}), 200
    else:
        return jsonify({"msg":"user not found"}), 404

@app.route('/user/<int:id>/favorite/people/<int:people_id>', methods = ['DELETE'])
def delete_favpeople(id, people_id):
    user = db.session.query(Usuario).get(id)
    personaje = db.session.query(Personaje).get(people_id)
    if user is not None and personaje is not None:
        user.followingPersonaje.remove(personaje)
        db.session.commit()
        return jsonify({"msg":"delete success"}), 200
    else:
        return jsonify({"msg":"user not found"}), 404


@app.route('/people', methods=['POST'])
def create_people():
    try:
        personaje = Personaje()
        personaje.id = request.json.get("id")
        personaje.nombre = request.json.get("nombre")
        personaje.rutaimagen = request.json.get("rutaimagen")
        personaje.genero = request.json.get("genero")
        personaje.colorpelo = request.json.get("colorpelo")
        personaje.colorojos = request.json.get("colorojos")
        personaje.nacimiento = request.json.get("nacimiento")
        personaje.altura = request.json.get("altura")
        personaje.colorpiel = request.json.get("colorpiel")
        print(personaje)
        db.session().add(personaje)
        db.session().commit()
        return jsonify({"message":"create People"}), 201
    except Exception as e:
        return jsonify({"message":e}), 500

@app.route('/people/<int:people_id>', methods = ['PUT'])
def update_people(people_id):
    personaje = db.session.query(Personaje).get(people_id)
    if personaje is not None:
        personaje.nombre = request.json.get("nombre")
        personaje.rutaimagen = request.json.get("rutaimagen")
        personaje.genero = request.json.get("genero")
        personaje.colorpelo = request.json.get("colorpelo")
        personaje.colorojos = request.json.get("colorojos")
        personaje.nacimiento = request.json.get("nacimiento")
        personaje.altura = request.json.get("altura")
        personaje.colorpiel = request.json.get("colorpiel")
        db.session.commit()
        return jsonify(personaje.serialize()), 200
    else:
        return jsonify({"message":"Personaje not found"}), 404

@app.route('/people/<int:people_id>', methods = ['DELETE'])
def delete_people(people_id):
    personaje = db.session.query(Personaje).get(people_id)
    print('Personaje:', personaje)
    if personaje is not None:
        users = personaje.followerPersonaje
        print('Usuarios:', users)
        for user in users:
            user.followingPersonaje.remove(personaje)
        db.session.delete(personaje)
        db.session.commit()
        return jsonify({"msg":"delete people success"}), 200
    else:
        return jsonify({"message":"People not found"}), 404

@app.route('/people', methods=['GET'])
def get_people():
    personajes = db.session.query(Personaje).all()
    print('Personajes',personajes)
    list_personaje = list()
    for personaje in personajes:
        print(personaje)
        print(personaje.nombre)
        print(personaje.genero)
        list_personaje.append(
            {
                "id": personaje.id,
                "nombre": personaje.nombre,
                "rutaimagen": personaje.rutaimagen,
                "genero": personaje.genero,
                "colorpelo": personaje.colorpelo,
                "colorrojos": personaje.colorrojos,
                "nacimiento": personaje.nacimiento,
                "altura": personaje.altura,
                "colorpiel": personaje.colorpiel
            }
        )
    print(personajes)
    return jsonify({"personajes": list_personaje}), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    personaje = db.session.query(Personaje).get(people_id)
    print('Personaje',personaje)
    if personaje is not None:
        return jsonify(personaje.serialize()), 200
    else:
        return jsonify({"message":"Personaje not found"}), 404


    # return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
