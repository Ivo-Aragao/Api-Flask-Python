from flask_restful import Resource, reqparse
from flask import jsonify
from models import db, Tutor, Pet, TutorSchema, PetSchema

class TutorResource(Resource):
    def get(self, tutor_id=None):
        if tutor_id is None:
            tutors = Tutor.query.all()
            return TutorSchema(many=True).dump(tutors), 200
        
        tutor = Tutor.query.get(tutor_id)
        return TutorSchema().dump(tutor), 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('none_tutor', type=str, required=True)
        args = parser.parse_arqs()
        tutor = Tutor(nome=args['nome_tutor'])
        db.session.add(tutor)
        db.session.commit()
        return TutorSchema().dump(tutor), 201
    
    def put(self, tutor_id):
        tutor = Tutor.query.get(tutor_id)
        if tutor:
            parser = reqparse.RequestParser()
            parser.add_argument('nome', type=str, required=True)
            args = parser.parse_args()
            
            tutor.nome = args['nome']
            db.session.commit()
            
            return TutorSchema().dump(tutor), 200
        else:
            return {'message': 'Tutor not found'}, 404

    def delete(self, tutor_id):
        tutor = Tutor.query.get(tutor_id)
        if tutor:
            db.session.delete(tutor)
            db.session.commit()
            return {'message': 'Tutor deleted'}, 204
        else:
            return {'message': 'Tutor not found'}, 404

    
class PetResource(Resource):
    def get(self, pet_id):
        pet = Pet.query.get(pet_id)
        return PetSchema().dump(pet), 200    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True)
        parser.add_argument('tutor_id', type=int, required=True)
        args = parser.parse_args()

        pet = Pet(nome=args['nome'], tutor_id=args['tutor_id'])
        db.session.add(pet)
        db.session.commit()
        return PetSchema().dump(pet), 201

    def put(self, pet_id):
        pet = Pet.query.get(pet_id)
        if pet:
            parser = reqparse.RequestParser()
            parser.add_argument('nome', type=str, required=True)
            parser.add_argument('tutor_id', type=int, required=True)
            args = parser.parse_args()
            
            pet.nome = args['nome']
            pet.tutor_id = args['tutor_id']
            db.session.commit()
            
            return PetSchema().dump(pet), 200
        else:
            return {'message': 'Pet not found'}, 404

    def delete(self, pet_id):
        pet = Pet.query.get(pet_id)
        if pet:
            db.session.delete(pet)
            db.session.commit()
            return {'message': 'Pet deleted'}, 204
        else:
            return {'message': 'Pet not found'}, 404
