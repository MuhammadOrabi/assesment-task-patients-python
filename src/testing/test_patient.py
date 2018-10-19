import unittest
import os
import json
from ..app import create_app, db


class PatientsTest(unittest.TestCase):
    """
    Patients Test Case
    """
    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.patient = {
            'name': 'olawale',
            'username': 'olawalemailcom',
            'password': 'passw0rd!'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_patient_creation(self):
        """ test patient creation with valid credentials """
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 201)

    def test_patient_creation_with_existing_username(self):
        """ test patient creation with already existing username"""
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    def test_patient_creation_with_no_password(self):
        """ test patient creation with no password"""
        patient1 = {
            'name': 'olawale',
            'username': 'olawale1mailcom',
        }
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(patient1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('password'))

    def test_patient_creation_with_no_username(self):
        """ test patient creation with no username """
        patient1 = {
            'name': 'olawale',
            'pasword': 'olawale1@mail.com',
        }
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(patient1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('username'))

    def test_patient_creation_with_empty_request(self):
        """ test patient creation with empty request """
        patient1 = {}
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(patient1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_patient_login(self):
        """ Patient Login Tests """
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/patients/login', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 200)

    def test_patient_login_with_invalid_password(self):
        """ patient Login Tests with invalid credentials """
        patient1 = {
            'password': 'olawale',
            'username': 'olawalemailcom',
        }
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/patients/login', headers={'Content-Type': 'application/json'}, data=json.dumps(patient1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_patient_login_with_invalid_username(self):
        """ Patient Login Tests with invalid credentials """
        patient1 = {
            'password': 'passw0rd!',
            'username': 'olawale1111mailcom',
        }
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/patients/login', headers={'Content-Type': 'application/json'}, data=json.dumps(patient1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_patient_get_me(self):
        """ Test Patient Get Me """
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().get('/api/patients/me', headers={'Content-Type': 'application/json', 'api-token': api_token})
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('username'), 'olawalemailcom')
        self.assertEqual(json_data.get('name'), 'olawale')

    def test_patient_update_me(self):
        """ Test Patient Update Me """
        patient1 = {
        'name': 'new name'
        }
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().put('/api/patients/me', headers={'Content-Type': 'application/json', 'api-token': api_token}, data=json.dumps(patient1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('name'), 'new name')

    def test_delete_patient(self):
        """ Test Patinet Delete """
        res = self.client().post('/api/patients/register', headers={'Content-Type': 'application/json'}, data=json.dumps(self.patient))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().delete('/api/patients/me', headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(res.status_code, 204)
        
    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
  unittest.main() 



