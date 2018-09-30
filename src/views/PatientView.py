#/src/views/PatientView

from flask import request, json, Response, Blueprint
from ..models.PatientModel import PatientModel, PatientSchema
from ..shared.Authentication import Auth


patient_api = Blueprint('patients', __name__)
patient_schema = PatientSchema()

@patient_api.route('/', methods=['POST'])
def create():
    """
    Create Patient Function
    """
    req_data = request.get_json()
    data, error = patient_schema.load(req_data)

    if error:
        return custom_response(error, 400)
    
    # check if user already exist in the db
    patient_in_db = PatientModel.get_patient_by_username(data.get('username'))
    if patient_in_db:
        message = {'error': 'Patient already exist, please supply another username'}
        return custom_response(message, 400)
    
    patient = PatientModel(data)
    patient.save()

    ser_data = patient_schema.dump(patient).data

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 201)

@patient_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    patients = PatientModel.get_all_patients()
    ser_patients = patient_schema.dump(patients, many=True).data
    return custom_response(ser_patients, 200)


@patient_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    data, error = patient_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)
    
    if not data.get('username') or not data.get('password'):
        return custom_response({'error': 'you need username and password to sign in'}, 400)
    
    patient = PatientModel.get_patient_by_username(data.get('username'))

    if not patient:
        return custom_response({'error': 'invalid credentials'}, 400)
    
    if not patient.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)
    
    ser_data = patient_schema.dump(patient).data
    
    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)

@patient_api.route('/<int:patient_id>', methods=['GET'])
@Auth.auth_required
def get_a_patient(patient_id):
    """
    Get a single patient
    """
    patient = PatientModel.get_one_patient(patient_id)
    if not patient:
        return custom_response({'error': 'patient not found'}, 404)
    
    ser_patient = patient_schema.dump(patient).data
    return custom_response(ser_patient, 200)

@patient_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)

    patient = PatientModel.get_one_patient(g.patient.get('id'))
    patient.update(data)
    ser_patient = patient_schema.dump(patient).data
    return custom_response(ser_patient, 200)

@patient_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
    Delete a patient
    """
    patient = PatientModel.get_one_patient(g.patient.get('id'))
    patient.delete()
    return custom_response({'message': 'deleted'}, 204)

@patient_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    """
    Get me
    """
    patient = PatientModel.get_one_patient(g.patient.get('id'))
    ser_patient = patient_schema.dump(patient).data
    return custom_response(ser_patient, 200)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )