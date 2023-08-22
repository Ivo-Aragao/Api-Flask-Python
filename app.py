from flask import Flask, request, jsonify
from flask_restful import Api
from models import db, Tutor, Pet  
from resources import TutorResource, PetResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)

@app.route('/tutors', methods=['GET'])
def list_tutors():
    tutors = Tutor.query.all()
    tutors_data = [{"id": tutor.id, "nome": tutor.nome} for tutor in tutors]
    return jsonify(tutors_data), 200

@app.route('/add_tutor', methods=['POST'])
def add_tutor():
    data = request.get_json()
    nome = data.get('nome')

    tutor = Tutor(nome=nome)
    db.session.add(tutor)
    db.session.commit()
    
    return jsonify({"message": "Tutor added successfully"}), 201

@app.route('/edit_tutor/<int:tutor_id>', methods=['PUT'])
def edit_tutor(tutor_id):
    tutor = Tutor.query.get(tutor_id)
    if tutor is None:
        return jsonify({"message": "Tutor not found"}), 404
    
    data = request.get_json()
    tutor.nome = data.get('nome')
    db.session.commit()
    
    return jsonify({"message": "Tutor updated successfully"}), 200

@app.route('/delete_tutor/<int:tutor_id>', methods=['DELETE'])
def delete_tutor(tutor_id):
    tutor = Tutor.query.get(tutor_id)
    if tutor is None:
        return jsonify({"message": "Tutor not found"}), 404
    
    db.session.delete(tutor)
    db.session.commit()
    
    return jsonify({"message": "Tutor deleted successfully"}), 204

@app.route('/pets', methods=['GET'])
def list_pets():
    pets = Pet.query.all()
    pets_data = [{"id": pet.id, "nome": pet.nome, "tutor_id": pet.tutor_id} for pet in pets]
    return jsonify(pets_data), 200

@app.route('/add_pet', methods=['POST'])
def add_pet():
    data = request.get_json()
    nome = data.get('nome')
    tutor_id = data.get('tutor_id')

    pet = Pet(nome=nome, tutor_id=tutor_id)
    db.session.add(pet)
    db.session.commit()
    
    return jsonify({"message": "Pet added successfully"}), 201

@app.route('/edit_pet/<int:pet_id>', methods=['PUT'])
def edit_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({"message": "Pet not found"}), 404
    
    data = request.get_json()
    pet.nome = data.get('nome')
    pet.tutor_id = data.get('tutor_id')
    db.session.commit()
    
    return jsonify({"message": "Pet updated successfully"}), 200

@app.route('/delete_pet/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({"message": "Pet not found"}), 404
    
    db.session.delete(pet)
    db.session.commit()
    
    return jsonify({"message": "Pet deleted successfully"}), 204
with app.app_context():
    db.create_all()

api.add_resource(TutorResource, '/tutor/<int:tutor_id>')
api.add_resource(PetResource, '/pet/<int:pet_id>')

if __name__ == '__main__':
    app.run()