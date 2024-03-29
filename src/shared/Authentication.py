#src/shared/Authentication
import jwt
import os
import datetime
from functools import wraps
from flask import json, Response, request, g
from ..models.PatientModel import PatientModel

class Auth():
    """
    Auth Class
    """
    @staticmethod
    def generate_token(patient_id):
        """
        Generate Token Method
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': patient_id
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET'),
                'HS256'
            ).decode("utf-8")
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'error in generating user token'}),
                status=400
            )
    
    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.getenv('SECRET'), algorithms=['HS256'])
            re['data'] = {'patient_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again with a new token'}
            return re


    # decorator
    @staticmethod
    def auth_required(func):
        """
        Auth decorator
        """
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )
        
            patient_id = data['data']['patient_id']
            check_patient = PatientModel.get_patient_by_id(patient_id)
            if not check_patient:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'patient does not exist, invalid token'}),
                    status=400
                )
            g.patient = {'id': patient_id}
            return func(*args, **kwargs)
            
        return decorated_auth