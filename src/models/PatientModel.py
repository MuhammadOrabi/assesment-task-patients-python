# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt


class PatientModel(db.Model):
    """
    Patient Model
    """

    # table name
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.username = data.get('username')
        self.password = self.__generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
    
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(item)
            setattr(self, key, item)

        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_patients():
        return PatientModel.query.all()
    
    @staticmethod
    def get_patient_by_id(id):
        return PatientModel.query.get(id)
    
    def __repr(self):
        return '<id {}>'.format(self.id)

# add this class
class PatientSchema(Schema):
    """
    Patient Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
