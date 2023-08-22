from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))  # Certifique-se de que 'nome' está definido aqui
    pets = db.relationship('Pet', backref='tutor', lazy=True)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome =  db.Column(db.String(100))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
       
class TutorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'pets') 

class PetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'tutor_id')              